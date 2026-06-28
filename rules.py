import json
from openai import OpenAI
import streamlit as st

from models import DecisionContext, Decision
from policy import get_policy


SYSTEM_PROMPT = """
You are Sentinel Enterprise Decision Intelligence.

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
