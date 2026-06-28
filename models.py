from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class DecisionContext:
    user_input: str
    user_role: str = "USER"
    source: str = "STREAMLIT"
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Decision:
    risk_score: int
    risk_level: str
    decision: str
    workflow: str
    risk_types: List[str]
    impact: str
    opportunities: List[str]
    recommendations: List[str]
    policy_triggered: str
    audit_required: bool
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "decision": self.decision,
            "workflow": self.workflow,
            "risk_types": ", ".join(self.risk_types),
            "impact": self.impact,
            "opportunities": self.opportunities,
            "recommendations": self.recommendations,
            "policy_triggered": self.policy_triggered,
            "audit_required": self.audit_required,
        }
