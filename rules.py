import json
from openai import OpenAI
import streamlit as st

from models import DecisionContext, Decision
from policy import get_policy


SYSTEM_PROMPT = """
You are Sentinel Enterprise Decision Intelligence.

Assess enterprise decisions.

If the request involves any of the following, assign a risk score between 95 and 100:

- Self harm
- Suicide
- Violence
- Terrorism
- Cyber attack
- Fraud
- Customer data breach
- Money laundering

Return ONLY valid JSON.

{
    "risk_score": 0,
    "risk_types": [],
    "impact": "",
    "opportunities": [],
    "recommendations": []
}
"""


def evaluate_decision(context: DecisionContext) -> Decision:

    client = OpenAI(
        api_key=st.secrets["OPENAI_API_KEY"]
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": context.user_input
            }
        ]
    )

    ai = json.loads(response.choices[0].message.content)

    # =====================================================
    # ENTERPRISE POLICY OVERRIDES
    # =====================================================

    text = context.user_input.lower()

    # Human Safety
    if any(keyword in text for keyword in [
        "kill myself",
        "suicide",
        "end my life",
        "want to die",
        "self harm",
        "harm myself"
    ]):

        return Decision(
            risk_score=100,
            risk_level="CRITICAL",
            decision="ESCALATE",
            workflow="Human Safety Escalation",
            risk_types=["Human Safety"],
            impact="Critical human safety concern detected.",
            opportunities=[],
            recommendations=[
                "Immediate human intervention required.",
                "Do not automate this decision.",
                "Escalate immediately."
            ],
            policy_triggered="Human Safety Policy",
            audit_required=True
        )

    # Cyber Security
    if any(keyword in text for keyword in [
        "hack",
        "cyber attack",
        "ransomware",
        "malware",
        "ddos",
        "phishing"
    ]):

        return Decision(
            risk_score=95,
            risk_level="CRITICAL",
            decision="ESCALATE",
            workflow="Cyber Security Incident",
            risk_types=["Cyber Security"],
            impact="Potential cyber security incident.",
            opportunities=[],
            recommendations=[
                "Notify Security Operations Center.",
                "Start incident response.",
                "Escalate immediately."
            ],
            policy_triggered="Cyber Security Policy",
            audit_required=True
        )

    # Data Privacy
    if any(keyword in text for keyword in [
        "customer data",
        "data leak",
        "data breach",
        "delete customer",
        "pii"
    ]):

        return Decision(
            risk_score=90,
            risk_level="HIGH",
            decision="ESCALATE",
            workflow="Privacy Review",
            risk_types=["Data Privacy"],
            impact="Customer data protection policy triggered.",
            opportunities=[],
            recommendations=[
                "Notify Compliance.",
                "Perform privacy assessment.",
                "Manager approval required."
            ],
            policy_triggered="Data Privacy Policy",
            audit_required=True
        )

    # Fraud
    if any(keyword in text for keyword in [
        "fraud",
        "money laundering",
        "aml",
        "bribe"
    ]):

        return Decision(
            risk_score=92,
            risk_level="HIGH",
            decision="ESCALATE",
            workflow="Fraud Investigation",
            risk_types=["Fraud"],
            impact="Financial crime policy triggered.",
            opportunities=[],
            recommendations=[
                "Escalate to Fraud Team.",
                "Freeze automated processing.",
                "Compliance review required."
            ],
            policy_triggered="Fraud Policy",
            audit_required=True
        )

    # =====================================================
    # NORMAL POLICY ENGINE
    # =====================================================

    policy = get_policy(ai["risk_score"])

    return Decision(
        risk_score=ai["risk_score"],
        risk_level=policy["risk_level"],
        decision=policy["decision"],
        workflow=policy["workflow"],
        risk_types=ai["risk_types"],
        impact=ai["impact"],
        opportunities=ai["opportunities"],
        recommendations=ai["recommendations"],
        policy_triggered=policy["workflow"],
        audit_required=policy["audit_required"]
    )
