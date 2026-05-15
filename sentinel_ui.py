import streamlit as st
from engine import analyze_decision

# ---------------- 1. PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sentinel",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- 2. STYLING (FIXED) ----------------
# The parameter MUST be 'unsafe_allow_html'
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00FFCC; }
    </style>
    """, 
    unsafe_allow_html=True
)

# ---------------- 3. HEADER ----------------
st.title("🛡️ Sentinel")
st.subheader("Universal AI Risk Decision Engine")
st.write("Analyze decisions, opportunities, and strategic moves before acting.")

# ---------------- 4. INPUT ----------------
user_input = st.text_area(
    "Decision Context",
    height=220,
    placeholder="Enter your input here..."
)

# ---------------- 5. ANALYSIS ----------------
if st.button("Analyze Risk"):
    if not user_input.strip():
        st.warning("Please enter an input.")
        st.stop()

    with st.spinner("Sentinel is analyzing..."):
        # Ensure engine.py is in the same folder on GitHub
        result = analyze_decision(user_input)

    if "error" in result:
        st.error(f"Engine Error: {result['error']}")
    else:
        # ---------------- 6. OUTPUT ----------------
        col1, col2 = st.columns(2)

        with col1:
            # We wrap in str() to ensure Streamlit metrics don't crash
            st.metric("Risk Level", str(result.get("risk_level", "N/A")))

        with col2:
            st.metric("Risk Score", f"{result.get('risk_score', 0)}/100")

        st.divider()

        st.subheader("Summary")
        st.write(result.get("summary", "No summary available."))

        st.subheader("Risk Types")
        st.write(result.get("risk_types", []))

        st.subheader("Key Concerns")
        st.write(result.get("key_concerns", "No concerns identified."))

        st.subheader("Opportunities")
        st.write(result.get("opportunities", []))

        st.subheader("Recommendations")
        st.write(result.get("recommendations", []))

        st.subheader("Final Verdict")
        st.success(result.get("final_verdict", "Analysis complete."))
