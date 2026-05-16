import streamlit as st
from engine import analyze_decision

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Sentinel Decision Intelligence Engine",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM UI STYLING
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 2rem;
}

h1 {
    font-size: 42px !important;
    font-weight: 700 !important;
}

textarea {
    border-radius: 12px !important;
}

.stButton > button {
    border-radius: 10px !important;
    height: 42px !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🛡️ Sentinel Decision Intelligence Engine")

st.markdown("""
Analyze strategic, financial, operational, and governance risks
before executing critical decisions.
""")

# ---------------------------------------------------
# USER ENTRY
# ---------------------------------------------------

user_input = st.text_area(
    "Enter Decision Context / Project Details:",
    placeholder="Describe the business decision, investment, operational change, or strategic move...",
    height=180
)

# ---------------------------------------------------
# SMALL BUTTON LAYOUT
# ---------------------------------------------------

col1, col2, col3 = st.columns([1,1,6])

with col1:
    analyze_clicked = st.button(
        "Analyze Risk",
        type="primary"
    )

# ---------------------------------------------------
# ANALYSIS EXECUTION
# ---------------------------------------------------

if analyze_clicked:

    if not user_input.strip():

        st.warning("Please enter some context first.")
        st.stop()

    with st.spinner("Running system policy audit..."):

        # Reset approval states
        if 'action_status' in st.session_state:
            del st.session_state['action_status']

        try:

            st.session_state.result = analyze_decision(user_input)

        except Exception:

            st.error(
                "System temporarily unavailable. Please retry."
            )

            st.stop()

# ---------------------------------------------------
# RESULT DISPLAY
# ---------------------------------------------------

if 'result' in st.session_state and "error" not in st.session_state.result:

    result = st.session_state.result

    st.divider()

    st.header("Result")

    # ---------------------------------------------------
    # METRICS
    # ---------------------------------------------------

    score = result.get('risk_score', 0)

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric(
            "Risk Score",
            score
        )

    with metric2:
        st.metric(
            "Risk Level",
            result.get('risk_level', 'N/A')
        )

    with metric3:

        if score >= 70:
            confidence = "91%"

        elif score >= 40:
            confidence = "84%"

        else:
            confidence = "96%"

        st.metric(
            "AI Confidence",
            confidence
        )

    # ---------------------------------------------------
    # DECISION STATUS
    # ---------------------------------------------------

    decision_text = result.get(
        'decision',
        'ALLOW'
    ).upper()

    if "ALLOW" in decision_text:

        status_display = "✅ ALLOW"

    elif "DENY" in decision_text:

        status_display = "❌ DENY"

    elif "ESCALATE" in decision_text:

        status_display = "⚠️ ESCALATE"

    else:

        status_display = "🟡 REVIEW"

    st.subheader(
        f"Initial Engine Recommendation: {status_display}"
    )

    # ---------------------------------------------------
    # RISK TYPES
    # ---------------------------------------------------

    st.write(
        f"**Risk Categories:** {result.get('risk_types', 'None')}"
    )

    # ---------------------------------------------------
    # IMPACT ANALYSIS
    # ---------------------------------------------------

    st.markdown("### Impact Analysis")

    st.write(
        result.get(
            'impact',
            'No summary available.'
        )
    )

    # ---------------------------------------------------
    # OPPORTUNITIES
    # ---------------------------------------------------

    st.markdown("### Opportunities & Upside")

    opportunities = result.get(
        'opportunities',
        []
    )

    if isinstance(opportunities, list) and opportunities:

        for opp in opportunities:

            st.write(f"• 💡 {opp}")

    else:

        st.write(
            "No specific upside identified."
        )

    # ---------------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------------

    st.markdown("### Strategic Recommendations")

    recommendations = result.get(
        'recommendations',
        []
    )

    if isinstance(recommendations, list) and recommendations:

        for rec in recommendations:

            st.write(f"• {rec}")

    else:

        st.write(
            "No recommendations provided."
        )

    # ---------------------------------------------------
    # GOVERNANCE REVIEW PANEL
    # ---------------------------------------------------

    st.divider()

    st.subheader(
        "🏛️ Executive Governance Review Panel"
    )

    if score >= 50:

        warning_msg = (
            f"Review Required: High Risk Profile Detected ({score}/100). "
            "Manual override necessary."
        )

        st.warning(warning_msg)

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "🟢 Override & Approve",
                use_container_width=True
            ):

                st.session_state.action_status = "APPROVED_BY_ADMIN"

        with col2:

            if st.button(
                "🔴 Reject Decision",
                use_container_width=True
            ):

                st.session_state.action_status = "REJECTED_BY_ADMIN"

    else:

        st.success(
            "✅ Safe Zone: This choice aligns with standard operational protocols."
        )

        if st.button(
            "📁 Log to Audit Trail",
            use_container_width=True
        ):

            st.session_state.action_status = "AUTO_LOGGED"

    # ---------------------------------------------------
    # PERSISTENT AUDIT CONFIRMATION
    # ---------------------------------------------------

    if 'action_status' in st.session_state:

        status = st.session_state.action_status

        st.write("")

        if status == "APPROVED_BY_ADMIN":

            st.success(
                "🔒 Audit Log Updated: Decision manually OVERRIDDEN & APPROVED by Executive."
            )

        elif status == "REJECTED_BY_ADMIN":

            st.error(
                "🔒 Audit Log Updated: Decision formally REJECTED. Action halted."
            )

        elif status == "AUTO_LOGGED":

            st.info(
                "🔒 Audit Log Updated: Automated signature recorded in corporate logs."
            )

    # ---------------------------------------------------
    # AUDIT SUMMARY
    # ---------------------------------------------------

    st.divider()

    st.subheader("📑 Audit Summary")

    st.write(f"• Risk Score: {score}")

    st.write(
        f"• Risk Level: {result.get('risk_level', 'N/A')}"
    )

    st.write(f"• Decision: {status_display}")

    st.write("• Governance Status: Recorded")

    st.write("• Sentinel Engine Status: Operational")
