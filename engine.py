from openai import OpenAI
import streamlit as st
import json

SYSTEM_PROMPT = """
You are Sentinel, an elite AI decision intelligence system.

Analyze the user input deeply.
Evaluate:
- Financial Risk
- Strategic Risk
- Operational Risk
- Reputation Risk
- Opportunity Cost
- Time Impact
- Human Dependency Risk
- Long-term Sustainability

CRITICAL RULE: You must return a valid JSON object ONLY. Do not wrap it in markdown code blocks like ```json. 
The JSON object must contain exactly these keys:
{
    "risk_level": "Low/Medium/High/Critical",
    "risk_score": 0-100 (as an integer),
    "summary": "Your dynamic text summary here",
    "risk_types": ["List", "of", "detected", "risks"],
    "key_concerns": "Your text here",
    "opportunities": ["List", "of", "opportunities"],
    "recommendations": ["List", "of", "actions"],
    "final_verdict": "Your final sign-off text"
}
"""

def analyze_decision(user_input):
    try:
        # MOVE THIS HERE: Initialize the client INSIDE the function safely
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the raw text response into a Python dictionary
        return json.loads(response.choices[0].message.content)
        
    except Exception as e:
        # If anything goes wrong, return the error message so your UI can display it
        return {"error": str(e)}
