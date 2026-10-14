"""
FR-003: Orchestrator.

Coordinates the Sentinel decision lifecycle end to end (PRD section 8):

  request -> validate -> knowledge retrieval -> AI reasoning
  -> decision engine -> policy engine -> resolution
  -> explainability + audit -> (human review?) -> outcome

The orchestrator coordinates; it deliberately contains no domain-specific
business logic of its own (FR-003) -- that all lives in config (FR-012)
and in the individual engines.

Every path -- success, business escalation, or technical failure -- writes
exactly one audit record, and a technical failure is always surfaced as an
explicit error status, never silently turned into a decision (section 23).
"""
from __future__ import annotations

import time

from . import ai_reasoning, audit, decision_engine, explainability, gateway, knowledge, policy_engine, resolver
from .errors import SentinelError, SystemError
from .human_review import check_escalation
from .models import AuditRecord, DecisionRequest, DecisionResponse
from .rules import get_field


def _build_knowledge_query(decision_type: str, context: dict, knowledge_cfg: dict) -> str:
    if "query" in knowledge_cfg:
        return knowledge_cfg["query"]
    fields = knowledge_cfg.get("query_fields", [])
    parts = [decision_type] + [str(get_field(context, f)) for f in fields if get_field(context, f) is not None]
    return " ".join(parts)


def run(payload: dict) -> dict:
    audit_id = audit.new_audit_id()
    request_for_audit: dict = dict(payload) if isinstance(payload, dict) else {"raw": str(payload)}

    try:
        req: DecisionRequest = gateway.parse_request(payload)
        request_for_audit = {
            "request_id": req.request_id,
            "decision_type": req.decision_type,
            "context": req.context,
            "metadata": req.metadata,
        }
    except SentinelError as e:
        audit.write(
            AuditRecord(
                audit_id=audit_id,
                request_id=request_for_audit.get("request_id", "UNKNOWN"),
                timestamp=time.time(),
                status=e.code,
                request=request_for_audit,
                evidence=[],
                ai_output=None,
                decision_engine_result=None,
                policy_results=[],
                resolution=None,
                explanation=None,
                config_versions={},
                error=e.to_dict(),
            )
        )
        return DecisionResponse(
            request_id=request_for_audit.get("request_id", "UNKNOWN"),
            status=e.code,
            outcome=None,
            confidence=None,
            ai_recommendation=None,
            policy_status="NOT_EVALUATED",
            evidence=[],
            explanation=None,
            audit_id=audit_id,
            error=e.to_dict(),
        ).to_dict()

    try:
        type_config = gateway.validate_request(req)

        knowledge_cfg = type_config.raw.get("knowledge", {})
        evidence = []
        if knowledge_cfg:
            query = _build_knowledge_query(req.decision_type, req.context, knowledge_cfg)
            evidence = knowledge.retrieve(
                query,
                sources=knowledge_cfg.get("sources"),
                top_k=knowledge_cfg.get("top_k", 5),
                min_relevance=knowledge_cfg.get("min_relevance", 0.15),
            )
            if knowledge_cfg.get("require_evidence") and not evidence:
                from .errors import InsufficientEvidenceError

                raise InsufficientEvidenceError(
                    "No evidence met the relevance threshold and this decision type requires evidence"
                )

        reasoner = ai_reasoning.get_reasoner()
        ai_output = reasoner.reason(req.decision_type, req.context, evidence, type_config.raw.get("ai_reasoning", {}))

        engine_result = decision_engine.evaluate(req.context, type_config.decision_engine)

        policy_results = policy_engine.evaluate_policies(req.context, type_config.policies)

        policy_failure_outcome = type_config.raw.get("policy_failure_outcome", "DECLINE")
        resolution = resolver.resolve(ai_output, engine_result, policy_results, policy_failure_outcome)

        escalation_reasons = check_escalation(
            context=req.context,
            ai_output=ai_output,
            resolution=resolution,
            insufficient_evidence=bool(knowledge_cfg) and not evidence,
            escalation_config=type_config.escalation,
        )
        human_review = None
        status = "COMPLETED"
        if escalation_reasons:
            status = "PENDING_HUMAN_REVIEW"
            human_review = {"triggered": True, "reasons": escalation_reasons, "proposed_outcome": resolution.final_outcome}

        explanation = explainability.build_explanation(
            evidence, ai_output, engine_result, policy_results, resolution, human_review, type_config.version
        )

        audit.write(
            AuditRecord(
                audit_id=audit_id,
                request_id=req.request_id,
                timestamp=time.time(),
                status=status,
                request=request_for_audit,
                evidence=[e.to_dict() for e in evidence],
                ai_output=ai_output.to_dict(),
                decision_engine_result=engine_result.to_dict(),
                policy_results=[p.to_dict() for p in policy_results],
                resolution=resolution.to_dict(),
                explanation=explanation.to_dict(),
                config_versions=explanation.config_versions,
            )
        )

        return DecisionResponse(
            request_id=req.request_id,
            status=status,
            outcome=resolution.final_outcome if status == "COMPLETED" else None,
            confidence=ai_output.confidence,
            ai_recommendation=ai_output.recommendation,
            policy_status=resolution.policy_status,
            evidence=[e.to_dict() for e in evidence],
            explanation=explanation.to_dict(),
            audit_id=audit_id,
        ).to_dict()

    except SentinelError as e:
        audit.write(
            AuditRecord(
                audit_id=audit_id,
                request_id=req.request_id,
                timestamp=time.time(),
                status=e.code,
                request=request_for_audit,
                evidence=[],
                ai_output=None,
                decision_engine_result=None,
                policy_results=[],
                resolution=None,
                explanation=None,
                config_versions={},
                error=e.to_dict(),
            )
        )
        return DecisionResponse(
            request_id=req.request_id,
            status=e.code,
            outcome=None,
            confidence=None,
            ai_recommendation=None,
            policy_status="NOT_EVALUATED",
            evidence=[],
            explanation=None,
            audit_id=audit_id,
            error=e.to_dict(),
        ).to_dict()
    except Exception as e:  # noqa: BLE001 -- last resort: never let a bug masquerade as a decision
        wrapped = SystemError(f"Unexpected error: {e}")
        audit.write(
            AuditRecord(
                audit_id=audit_id,
                request_id=req.request_id,
                timestamp=time.time(),
                status=wrapped.code,
                request=request_for_audit,
                evidence=[],
                ai_output=None,
                decision_engine_result=None,
                policy_results=[],
                resolution=None,
                explanation=None,
                config_versions={},
                error=wrapped.to_dict(),
            )
        )
        return DecisionResponse(
            request_id=req.request_id,
            status=wrapped.code,
            outcome=None,
            confidence=None,
            ai_recommendation=None,
            policy_status="NOT_EVALUATED",
            evidence=[],
            explanation=None,
            audit_id=audit_id,
            error=wrapped.to_dict(),
        ).to_dict()
