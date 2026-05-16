from openai import OpenAI
import streamlit as st
import json

SYSTEM_PROMPT = """
You are Sentinel, an elite AI decision and risk intelligence system.
Analyze the user input deeply and evaluate the operational, financial, and strategic risks.

CRITICAL RULE: You must return a valid JSON object ONLY. Do not wrap it in markdown code blocks like ```json.
The JSON object must contain exactly these keys with appropriate types:
{
    "risk_score": 0-100 (as an integer),
    "risk_level": "Low/Medium/High/Critical",
    "decision": "ALLOW or DENY",
    "risk_types": "Financial, Strategic, Operational, etc. (as a single string)",
    "impact": "A concise summary of the decision impact",
    "opportunities": ["List item 1", "List item 2"],
    "recommendations": ["List item 1", "List item 2"]
}
"""

def analyze_decision(user_input):
    try:
        # Initialized safely inside the function block to prevent boot-up errors
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
