import json
import streamlit as st
from openai import OpenAI

from models import DecisionContext, Decision
from policy import get_policy


SYSTEM_PROMPT = """
You are Sentinel Enterprise Decision Intelligence.

You are an Enterprise Risk and Governance Analyst.

Analyse every business decision like an enterprise Risk Committee.

Return ONLY valid JSON.

Schema

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

Guidelines

1. Identify the Business Domain.
2. Identify the Business Intent.
3. Identify the Decision Type.
4. Assess the Overall Risk.
5. Assign Severity.
6. Determine whether Human Review is required.
7. Provide meaningful Risk Types.
8. Describe Business Impact.
9. Suggest Business Opportunities.
10. Give Executive Recommendations.

Risk Score Mapping

LOW = 0-30

MEDIUM = 31-60

HIGH = 61-80

CRITICAL = 81-100

Return ONLY valid JSON.
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

    severity = ai.get(
        "severity",
        "MEDIUM"
    ).upper()

    requires_human_review = ai.get(
        "requires_human_review",
        severity in ["HIGH", "CRITICAL"]
    )

    policy = get_policy(
        severity=severity,
        requires_human_review=requires_human_review
    )

    return Decision(

        domain=ai.get(
            "domain",
            "General Business"
        ),

        intent=ai.get(
            "intent",
            "Business Decision"
        ),

        decision_type=ai.get(
            "decision_type",
            "General Decision"
        ),

        risk_score=ai.get(
            "risk_score",
            50
        ),

        risk_level=policy["risk_level"],

        decision=policy["decision"],

        workflow=policy["workflow"],

        policy_triggered=policy["workflow"],

        audit_required=policy["audit_required"],

        risk_types=ai.get(
            "risk_types",
            []
        ),

        impact=ai.get(
            "impact",
            "No business impact identified."
        ),

        opportunities=ai.get(
            "opportunities",
            []
        ),

        recommendations=ai.get(
            "recommendations",
            []
        )

    )
