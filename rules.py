import json
import streamlit as st
from openai import OpenAI

from models import DecisionContext, Decision
from policy import get_policy


SYSTEM_PROMPT = """
You are Sentinel Enterprise Decision Intelligence.

Your task is to classify enterprise decisions.

Return ONLY valid JSON.

{
    "domain": "",
    "intent": "",
    "decision_type": "",
    "severity": "LOW | MEDIUM | HIGH | CRITICAL",
    "risk_score": 0,
    "risk_types": [],
    "requires_human_review": false,
    "impact": "",
    "opportunities": [],
    "recommendations": []
}

Guidelines:

- Understand the business context.
- Classify the domain.
- Identify the business intent.
- Determine the decision type.
- Assess severity.
- Decide if human review is required.
- Assign an appropriate risk score.
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

    ai = json.loads(
        response.choices[0].message.content
    )

    policy = get_policy(

        severity=ai["severity"],

        requires_human_review=ai["requires_human_review"]

    )

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
