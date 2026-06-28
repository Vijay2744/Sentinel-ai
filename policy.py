def get_policy(score: int):

    if score >= 80:
        return {
            "risk_level": "Critical",
            "decision": "REJECT",
            "workflow": "Executive Review",
            "audit_required": True
        }

    elif score >= 60:
        return {
            "risk_level": "High",
            "decision": "ESCALATE",
            "workflow": "Senior Approval",
            "audit_required": True
        }

    elif score >= 40:
        return {
            "risk_level": "Medium",
            "decision": "REVIEW",
            "workflow": "Manager Review",
            "audit_required": True
        }

    else:
        return {
            "risk_level": "Low",
            "decision": "APPROVE",
            "workflow": "Straight Through Processing",
            "audit_required": False
        }
