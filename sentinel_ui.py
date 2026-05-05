import streamlit as st
import requests

# -------------------------------
# CONFIG
# -------------------------------
API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="Sentinel",
    page_icon="🛡️",
    layout="centered"
)

# -------------------------------
# UI HEADER
# -------------------------------
st.title("🛡️ Sentinel")
st.subheader("Universal AI Risk Decision Engine")

st.markdown(
    "Analyze any important decision before you act."
)

# -------------------------------
# INPUT
# -------------------------------
user_input = st.text_area(
    "Enter your decision:",
    placeholder="e.g. Take 10 lakhs loan and invest in stocks"
)

# -------------------------------
# BUTTON ACTION
# -------------------------------
if st.button("Analyze Risk"):

    if not user_input.strip():
        st.warning("Please enter a decision")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"decision": user_input},  # IMPORTANT FIX
                    timeout=10
                )

                if response.status_code != 200:
                    st.error(f"API Error: {response.status_code}")
                    st.write(response.text)
                else:
                    result = response.json()

                    # -------------------------------
                    # RESULT DISPLAY
                    # -------------------------------
                    st.success("Analysis Complete")

                    st.markdown("## 📊 Result")

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Risk Score", result["risk_score"])
                    col2.metric("Risk Level", result["risk_level"])
                    col3.metric("Decision", result["decision"])

                    st.markdown("### ⚠️ Risk Types")
                    for r in result["risk_types"]:
                        st.write(f"- {r}")

                    st.markdown("### 🧠 Explanation")
                    st.write(result["explanation"])

                    st.markdown("### ✅ Recommendations")
                    for rec in result["recommendations"]:
                        st.write(f"- {rec}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to API. Make sure FastAPI is running on port 8000.")

            except Exception as e:
                st.error(f"Unexpected error: {e}")
