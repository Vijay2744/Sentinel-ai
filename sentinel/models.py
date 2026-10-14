"""
Core data structures shared across the Sentinel pipeline.
Deliberately plain dataclasses (no pydantic/fastapi dependency) so this
package runs anywhere with just the Python standard library. Swap in
pydantic models with the same field names if/when you move to FastAPI.
"""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Optional


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12]}"


@dataclass
class DecisionRequest:
    """FR-001: the inbound decision request."""
    decision_type: str
    context: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    request_id: Optional[str] = None
    idempotency_key: Optional[str] = None

    def __post_init__(self):
        if not self.request_id:
            self.request_id = new_id("REQ")


@dataclass
class EvidenceItem:
    """FR-004: a single piece of retrieved knowledge, with provenance."""
    source: str
    version: str
    section: str
    content: str
    relevance_score: float

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AIOutput:
    """FR-005: structured AI reasoning output. Never the final outcome."""
    recommendation: Any
    confidence: float
    reasoning_summary: str
    evidence_ids: list = field(default_factory=list)
    model: str = "stub-reasoner-v1"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DecisionEngineResult:
    """FR-006: deterministic, reproducible decision-logic output."""
    outcome: Any
    score: Optional[float]
    rule_trace: list = field(default_factory=list)  # [{"rule": "...", "result": "..."}]
    config_version: str = "unversioned"

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PolicyRuleResult:
    rule_id: str
    description: str
    passed: bool
    detail: str = ""


@dataclass
class PolicyResult:
    """FR-007: outcome of evaluating one or more policies."""
    policy_id: str
    version: str
    rules: list = field(default_factory=list)  # list[PolicyRuleResult]

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.rules)

    def to_dict(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "version": self.version,
            "passed": self.passed,
            "rules": [asdict(r) for r in self.rules],
        }


@dataclass
class Resolution:
    """FR-008: the governed final outcome and why it was reached."""
    final_outcome: Any
    ai_recommendation: Any
    decision_engine_outcome: Any
    policy_status: str  # PASS | FAIL | OVERRIDDEN_BY_POLICY
    overridden: bool
    override_reason: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Explanation:
    """FR-009: structured, execution-grounded explanation."""
    final_outcome: Any
    ai_recommendation: Any
    evidence: list
    rules_evaluated: list
    policies_evaluated: list
    overrides: list
    human_intervention: Optional[dict]
    config_versions: dict

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AuditRecord:
    """FR-010: everything needed to reconstruct the decision lifecycle."""
    audit_id: str
    request_id: str
    timestamp: float
    status: str
    request: dict
    evidence: list
    ai_output: Optional[dict]
    decision_engine_result: Optional[dict]
    policy_results: list
    resolution: Optional[dict]
    explanation: Optional[dict]
    config_versions: dict
    error: Optional[dict] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class DecisionResponse:
    """The Decision Contract (section 22 of the PRD)."""
    request_id: str
    status: str
    outcome: Any
    confidence: Optional[float]
    ai_recommendation: Any
    policy_status: str
    evidence: list
    explanation: Optional[dict]
    audit_id: Optional[str]
    error: Optional[dict] = None

    def to_dict(self) -> dict:
        return asdict(self)
