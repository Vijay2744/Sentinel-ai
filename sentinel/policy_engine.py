"""
FR-007: Policy Engine -- mandatory organizational constraints.

Policies are deterministic and versioned. A policy fails if any one of its
rules fails. Policy evaluation always runs even if a policy rule would
technically allow the same outcome the decision engine reached -- the
point is independent, auditable confirmation, not a shortcut.

Policy file shape (config/policies/<policy_id>.json):
  {
    "policy_id": "kyc_mandatory",
    "version": "1.0",
    "active": true,
    "rules": [
      {"id": "P1", "description": "KYC must be verified", "field": "kyc_status", "op": "==", "value": "VERIFIED"}
    ]
  }
"""
from __future__ import annotations

from . import config
from .errors import PolicyEngineError
from .models import PolicyResult, PolicyRuleResult
from .rules import evaluate_condition


def evaluate_policy(context: dict, policy_id: str) -> PolicyResult:
    try:
        policy = config.load_policy(policy_id)
    except config.ConfigError as e:
        raise PolicyEngineError(f"Policy not found: {policy_id}") from e

    if not policy.get("active", True):
        # An inactive policy auto-passes but is still recorded for audit.
        return PolicyResult(policy_id=policy_id, version=policy.get("version", "unversioned"), rules=[
            PolicyRuleResult(rule_id="(inactive)", description="Policy deactivated", passed=True, detail="skipped")
        ])

    results = []
    for rule in policy.get("rules", []):
        try:
            passed, detail = evaluate_condition(context, rule)
        except (KeyError, ValueError) as e:
            raise PolicyEngineError(f"Malformed policy rule {rule.get('id')} in {policy_id}: {e}") from e
        results.append(
            PolicyRuleResult(
                rule_id=rule.get("id", "unnamed"),
                description=rule.get("description", ""),
                passed=passed,
                detail=detail,
            )
        )
    return PolicyResult(policy_id=policy_id, version=policy.get("version", "unversioned"), rules=results)


def evaluate_policies(context: dict, policy_ids: list[str]) -> list[PolicyResult]:
    return [evaluate_policy(context, pid) for pid in policy_ids]
