"""
FR-008: Decision Resolution.

Precedence, per the PRD's own worked example (section 17) and principle
5.1 ("AI assists; Sentinel governs"):

    Policy Engine  >  Decision Engine  >  AI recommendation

The AI's recommendation is informational and is always recorded, but it
never determines the governed outcome by itself, and a failing policy
always overrides whatever the deterministic decision engine produced.
The resolver records *why* the final outcome differs from the AI
recommendation whenever it does, per FR-008's explicit requirement.
"""
from __future__ import annotations

from .models import AIOutput, DecisionEngineResult, PolicyResult, Resolution


def resolve(
    ai_output: AIOutput,
    engine_result: DecisionEngineResult,
    policy_results: list[PolicyResult],
    policy_failure_outcome: str = "DECLINE",
) -> Resolution:
    all_policies_passed = all(p.passed for p in policy_results)

    if all_policies_passed:
        final_outcome = engine_result.outcome
        policy_status = "PASS"
        overridden_by_policy = False
        override_reason = ""
    else:
        final_outcome = policy_failure_outcome
        policy_status = "FAIL"
        overridden_by_policy = final_outcome != engine_result.outcome
        failed = [
            f"{p.policy_id} v{p.version}: " + ", ".join(r.rule_id for r in p.rules if not r.passed)
            for p in policy_results
            if not p.passed
        ]
        override_reason = "Policy failure overrides decision engine outcome: " + "; ".join(failed)

    return Resolution(
        final_outcome=final_outcome,
        ai_recommendation=ai_output.recommendation,
        decision_engine_outcome=engine_result.outcome,
        policy_status=policy_status,
        overridden=overridden_by_policy,
        override_reason=override_reason,
    )
