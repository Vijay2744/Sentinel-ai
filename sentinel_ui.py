import streamlit as st
from engine import analyze_decision

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="Sentinel",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- HEADER ----------------

st.title("🛡️ Sentinel")

st.subheader(
    "Universal AI Risk Decision Engine"
)

st.write(
    "Analyze decisions, opportunities, risks, and strategic moves before acting."
)

# ---------------- INPUT ----------------

user_input = st.text_area(
    "",
    height=220,
    placeholder="Enter your input..."
)

# ---------------- BUTTON ----------------

if st.button("Analyze Risk"):

    if not user_input.strip():

        st.warning("Please enter an input.")

        st.stop()

    with st.spinner("Sentinel is analyzing..."):

        result = analyze_decision(user_input)

    # ---------------- OUTPUT ----------------

    if "error" in result:

        st.error(result["error"])

    else:

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Risk Level",
                result["risk_level"]
            )

        with col2:
            st.metric(
                "Risk Score",
                result["risk_score"]
            )

        st.subheader("Summary")
        st.write(result["summary"])

        st.subheader("Risk Types")
        st.write(result["risk_types"])

        st.subheader("Key Concerns")
        st.write(result["key_concerns"])

        st.subheader("Opportunities")
        st.write(result["opportunities"])

        st.subheader("Recommendations")
        st.write(result["recommendations"])

        st.subheader("Final Verdict")
        st.success(result["final_verdict"])
