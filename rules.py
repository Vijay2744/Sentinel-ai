from datetime import datetime

from policy import POLICY
from models import Decision


def check_rule(action, approved, role):

    rule = POLICY.get(action)

    if not rule:
        return Decision(
            action=action,
            role=role,
            decision="DENY",
            reason="Unknown action",
            risk="UNKNOWN",
            timestamp=datetime.now()
        )

    risk = rule["risk"]
    requires_approval = rule["requires_approval"]

    # Role-based restriction
    if role == "ANALYST" and risk in ["HIGH", "CRITICAL"]:
        return Decision(
            action=action,
            role=role,
            decision="DENY",
            reason="Role not allowed for high risk",
            risk=risk,
            timestamp=datetime.now()
        )

    # Low risk always allowed
    if risk == "LOW":
        return Decision(
            action=action,
            role=role,
            decision="ALLOW",
            reason="Low risk action",
            risk=risk,
            timestamp=datetime.now()
        )

    # Approval check
    if requires_approval and not approved:
        return Decision(
            action=action,
            role=role,
            decision="DENY",
            reason="Approval required",
            risk=risk,
            timestamp=datetime.now()
        )

    # Critical always blocked
    if risk == "CRITICAL":
        return Decision(
            action=action,
            role=role,
            decision="DENY",
            reason="Critical actions blocked",
            risk=risk,
            timestamp=datetime.now()
        )

    return Decision(
        action=action,
        role=role,
        decision="ALLOW",
        reason="Allowed by policy",
        risk=risk,
        timestamp=datetime.now()
    )
