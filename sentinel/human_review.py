"""
FR-011: Human Review.

Not every decision should be fully automated (principle 5.6). This module
only decides WHETHER to escalate -- it never performs the review itself.
In this MVP, an escalated decision is parked in PENDING_HUMAN_REVIEW status
with its proposed outcome recorded; wiring a real reviewer queue/UI is a
follow-on, not a platform change (see README).

Config shape (decision_type config's "escalation" key):
  {
    "min_confidence": 0.6,
    "mandatory_review_outcomes": ["REVIEW"],
    "escalate_on_conflict": true,
    "max_auto_approve": {"field": "requested_amount", "value": 5000000}
  }
All keys optional -- an empty escalation config means "never escalate".
"""
from __future__ import annotations

from .models import AIOutput, Resolution
from .rules import get_field


def check_escalation(
    context: dict,
    ai_output: AIOutput,
    resolution: Resolution,
    insufficient_evidence: bool,
    escalation_config: dict,
) -> list[str]:
    reasons: list[str] = []

    if insufficient_evidence:
        reasons.append("Insufficient evidence to support a confident recommendation")

    min_conf = escalation_config.get("min_confidence")
    if min_conf is not None and ai_output.confidence < min_conf:
        reasons.append(f"AI confidence {ai_output.confidence} below threshold {min_conf}")

    mandatory = escalation_config.get("mandatory_review_outcomes", [])
    if resolution.final_outcome in mandatory:
        reasons.append(f"Outcome '{resolution.final_outcome}' requires mandatory human approval")

    if escalation_config.get("escalate_on_conflict") and (
        ai_output.recommendation != resolution.decision_engine_outcome
    ):
        reasons.append(
            f"AI recommendation ({ai_output.recommendation}) conflicts with "
            f"decision engine outcome ({resolution.decision_engine_outcome})"
        )

    cap = escalation_config.get("max_auto_approve")
    if cap:
        value = get_field(context, cap["field"])
        if isinstance(value, (int, float)) and value > cap["value"]:
            reasons.append(f"{cap['field']}={value} exceeds auto-approve cap {cap['value']}")

    return reasons
