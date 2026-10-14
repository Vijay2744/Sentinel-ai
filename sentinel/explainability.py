"""
FR-009: Explainability.

The explanation is assembled entirely from structured execution data that
the pipeline already produced -- evidence, rule trace, policy results,
overrides, human intervention. Nothing here is a free-form LLM narrative;
if you want prose for an end user, generate it FROM this structure as a
presentation step, never as a replacement for it.
"""
from __future__ import annotations

from .models import (
    AIOutput,
    DecisionEngineResult,
    EvidenceItem,
    Explanation,
    PolicyResult,
    Resolution,
)


def build_explanation(
    evidence: list[EvidenceItem],
    ai_output: AIOutput,
    engine_result: DecisionEngineResult,
    policy_results: list[PolicyResult],
    resolution: Resolution,
    human_review: dict | None,
    decision_type_version: str,
) -> Explanation:
    overrides = []
    if resolution.overridden:
        overrides.append(
            {
                "overridden_outcome": resolution.decision_engine_outcome,
                "final_outcome": resolution.final_outcome,
                "reason": resolution.override_reason,
            }
        )

    return Explanation(
        final_outcome=resolution.final_outcome,
        ai_recommendation=ai_output.recommendation,
        evidence=[e.to_dict() for e in evidence],
        rules_evaluated=engine_result.rule_trace,
        policies_evaluated=[p.to_dict() for p in policy_results],
        overrides=overrides,
        human_intervention=human_review,
        config_versions={
            "decision_type": decision_type_version,
            "decision_engine": engine_result.config_version,
            "policies": {p.policy_id: p.version for p in policy_results},
        },
    )
