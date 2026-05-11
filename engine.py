from openai import OpenAI
import streamlit as st
import json

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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

Return clean JSON only.
"""

def analyze_decision(user_input):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.7
    )

    output = response.choices[0].message.content

    try:
        return json.loads(output)
    except:
        return {"response": output}
