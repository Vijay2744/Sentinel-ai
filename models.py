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

    # Enterprise Classification
    domain: str
    intent: str
    decision_type: str

    # Risk Assessment
    risk_score: int
    risk_level: str

    # Governance
    decision: str
    workflow: str
    policy_triggered: str
    audit_required: bool

    # AI Insights
    risk_types: List[str]
    impact: str
    opportunities: List[str]
    recommendations: List[str]

    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self):

        return {

            "domain": self.domain,
            "intent": self.intent,
            "decision_type": self.decision_type,

            "risk_score": self.risk_score,
            "risk_level": self.risk_level,

            "decision": self.decision,
            "workflow": self.workflow,

            "policy_triggered": self.policy_triggered,
            "audit_required": self.audit_required,

            "risk_types": self.risk_types,

            "impact": self.impact,

            "opportunities": self.opportunities,

            "recommendations": self.recommendations

        }
