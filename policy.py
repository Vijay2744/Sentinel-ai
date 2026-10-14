"""
Sentinel Enterprise Policy Engine

The Policy Engine is responsible only for converting
AI classifications into enterprise governance decisions.

It never interprets raw user input.
It never performs keyword matching.
"""


def get_policy(
    severity: str,
    requires_human_review: bool
):

    severity = severity.upper().strip()

    POLICY = {

        "LOW": {
            "risk_level": "Low",
            "decision": "APPROVE",
            "workflow": "Straight Through Processing",
            "audit_required": False
        },

        "MEDIUM": {
            "risk_level": "Medium",
            "decision": "REVIEW",
            "workflow": "Manager Review",
            "audit_required": True
        },

        "HIGH": {
            "risk_level": "High",
            "decision": "ESCALATE",
            "workflow": "Senior Approval",
            "audit_required": True
        },

        "CRITICAL": {
            "risk_level": "Critical",
            "decision": "REJECT",
            "workflow": "Executive Review",
            "audit_required": True
        }

    }

    policy = POLICY.get(
        severity,
        POLICY["MEDIUM"]
    )

    # Optional governance override
    if requires_human_review:

        policy["audit_required"] = True

    return policy
