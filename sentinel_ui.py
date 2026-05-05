import streamlit as st
import requests

# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="Sentinel",
    page_icon="🛡️",
    layout="centered"
)

# -------- UI --------
st.title("🛡️ Sentinel")
st.subheader("Universal AI Risk Decision Engine")

st.markdown("Analyze any important decision before you act.")

# -------- INPUT --------
user_input = st.text_area(
    "Enter your decision:",
    placeholder="Example: Should I quit my job to start a startup?"
)

# -------- BUTTON --------
if st.button("Analyze Risk"):

    if not user_input.strip():
        st.warning("Please enter a decision.")
        st.stop()

    with st.spinner("Analyzing..."):

        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"decision": user_input}
            )

            data = response.json()

            if "error" in data:
                st.error("API Error")
                st.code(data)
                st.stop()

            # -------- RESULT --------
            st.success("Analysis Complete")

            st.markdown("## Result")

            st.metric("Risk Score", data.get("risk_score"))

            st.write("**Risk Level:**", data.get("risk_level"))
            st.write("**Decision:**", data.get("decision"))

            st.write("**Risk Types:**", ", ".join(data.get("risk_types", [])))

            st.write("**Explanation:**")
            st.write(data.get("explanation"))

            st.write("**Recommendations:**")
            for rec in data.get("recommendations", []):
                st.write("-", rec)

        except Exception as e:
            st.error("Failed to call API")
            st.code(str(e))
