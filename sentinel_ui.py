import streamlit as st
from openai import OpenAI
import json

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sentinel",
    page_icon="🛡️",
    layout="centered"
)

# ---------------- OPENAI ----------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ---------------- UI ----------------
st.title("🛡️ Sentinel")
st.subheader("Universal AI Risk Decision Engine")

st.markdown(
    "Analyze any important decision before you act."
)

# ---------------- INPUT ----------------
user_input = st.text_area(
    "Enter your decision:",
    placeholder="Describe the decision you want evaluated"
)

# ---------------- BUTTON ----------------
if st.button("Analyze Risk"):

    if not user_input.strip():
        st.warning("Please enter a decision.")
        st.stop()

    with st.spinner("Analyzing..."):

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Sentinel, an elite decision-risk analyst.

Analyze any user decision dynamically.

Evaluate these dimensions:
1. Financial Risk
2. Strategic Risk
3. Operational Risk
4. Reputation Risk
5. Opportunity Cost
6. Uncertainty Risk
7. Time Impact
8. Dependency / Human Risk

Return STRICT JSON only:

{
  "risk_level": "Low/Medium/High",
  "risk_score": 0,
  "risk_types": ["Strategic","Financial"],
  "impact": "Short explanation",
  "recommendations": ["Point 1","Point 2","Point 3"]
}

Rules:
- risk_score must be integer 0 to 100
- Low = 0-39
- Medium = 40-69
- High = 70-100
- Keep concise
"""
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        output = response.choices[0].message.content

        try:
            data = json.loads(output)

            risk_score = int(data.get("risk_score", 50))
            risk_level = data.get("risk_level", "Medium")

            if risk_score >= 70:
                decision = "❌ REJECT"
            elif risk_score >= 40:
                decision = "⚠️ REVIEW"
            else:
                decision = "✅ ALLOW"

            st.success("Analysis Complete")

            st.markdown("## Result")

            st.metric("Risk Score", risk_score)

            st.write("**Risk Level:**", risk_level)
            st.write("**Decision:**", decision)
            st.write(
                "**Risk Types:**",
                ", ".join(data.get("risk_types", []))
            )
            st.write("**Impact:**", data.get("impact", ""))

            st.write("**Recommendations:**")
            for rec in data.get("recommendations", []):
                st.write("-", rec)

        except:
            st.error("Failed to parse AI response")
            st.code(output)
