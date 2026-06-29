import json
import streamlit as st
from openai import OpenAI

from models import DecisionContext, Decision
from policy import get_policy


SYSTEM_PROMPT = """
You are Sentinel Enterprise Decision Intelligence.

You are an enterprise AI decision analyst.

Your responsibility is to analyse a business decision and classify it for enterprise governance.

Return ONLY valid JSON in the following format.

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

Rules:

1. Risk Score must always be between 0 and 100.

2. Severity must match Risk Score.

LOW:
0-30

MEDIUM:
31-60

HIGH:
61-80

CRITICAL:
81-100

3. HIGH and CRITICAL decisions must require human review.

4. Risk Types must support the selected severity.

5. Recommendations must align with the identified risks.

6. Do not generate contradictory outputs.

7. Return ONLY valid JSON.
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

    severity = ai.get("severity", "MEDIUM").upper()

    requires_human_review = ai.get(
        "requires_human_review",
        severity in ["HIGH", "CRITICAL"]
    )

    policy = get_policy(
        severity=severity,
        requires_human_review=requires_human_review
    )

    return Decision(

        risk_score=ai.get("risk_score", 50),

        risk_level=policy["risk_level"],

        decision=policy["decision"],

        workflow=policy["workflow"],

        risk_types=ai.get("risk_types", []),

        impact=ai.get(
            "impact",
            "No impact assessment available."
        ),

        opportunities=ai.get(
            "opportunities",
            []
        ),

        recommendations=ai.get(
            "recommendations",
            []
        ),

        policy_triggered=policy["workflow"],

        audit_required=policy["audit_required"]

    )
