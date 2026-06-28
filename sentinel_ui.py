import streamlit as st
from engine import analyze_decision

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sentinel Enterprise Decision Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# --------------------------------------------------
# STYLING
# --------------------------------------------------

st.markdown("""
<style>

.main .block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    color:#0E4D92;
    font-size:40px;
    font-weight:700;
}

h2{
    color:#1B263B;
}

.stButton>button{
    width:100%;
    height:48px;
    border-radius:8px;
    font-weight:600;
}

.metric-card{
    background:#F8F9FA;
    border:1px solid #E6E6E6;
    border-radius:12px;
    padding:15px;
}

.audit-box{
    background:#F5F7FA;
    border-left:5px solid #0E4D92;
    padding:12px;
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🛡️ Sentinel Enterprise Decision Intelligence")

st.caption(
    "AI Decision Engine • Enterprise Risk • Governance • Policy Intelligence"
)

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

st.subheader("Decision Context")

user_input = st.text_area(

    label="Describe your business decision",

    height=220,

    placeholder="""
Examples

• Launch Loan Against Securities for NRIs

• Increase LTV from 50% to 65%

• Approve ₹50 Crore investment

• Delete customer data

• Launch AI Credit Underwriting

• Enter a new market
"""
)

left, middle, right = st.columns([2,1,7])

with left:

    analyze = st.button(
        "Analyze Decision",
        type="primary"
    )

# --------------------------------------------------
# EXECUTE ENGINE
# --------------------------------------------------

if analyze:

    if not user_input.strip():

        st.warning("Please enter a decision.")

        st.stop()

    with st.spinner("Running Sentinel Decision Engine..."):

        st.session_state.result = analyze_decision(user_input)

# --------------------------------------------------
# EXECUTIVE DECISION DASHBOARD
# --------------------------------------------------

if "result" in st.session_state:

    result = st.session_state.result

    if "error" in result:

        st.error(result["error"])

        st.stop()

    score = result.get("risk_score", 0)

    risk_level = result.get("risk_level", "N/A")

    decision = result.get("decision", "REVIEW")

    workflow = result.get("workflow", "N/A")

    policy = result.get("policy_triggered", "N/A")

    audit_required = result.get("audit_required", False)

    audit_id = result.get("audit_id", "N/A")

    # ---------------------------------------------
    # AI Confidence
    # ---------------------------------------------

    if score >= 80:
        confidence = "95%"

    elif score >= 60:
        confidence = "91%"

    elif score >= 40:
        confidence = "87%"

    else:
        confidence = "98%"

    # ---------------------------------------------
    # Decision Status
    # ---------------------------------------------

    decision_map = {

        "APPROVE": ("✅", st.success),

        "REVIEW": ("🟡", st.warning),

        "ESCALATE": ("⚠️", st.warning),

        "REJECT": ("❌", st.error)

    }

    icon, display = decision_map.get(
        decision,
        ("❓", st.info)
    )

    st.divider()

    st.header("Executive Decision Dashboard")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Risk Score", f"{score}/100")

    with m2:
        st.metric("Risk Level", risk_level)

    with m3:
        st.metric("Workflow", workflow)

    with m4:
        st.metric("AI Confidence", confidence)
    display(f"{icon} {decision}")

    st.caption(
        f"Workflow: {workflow} | Policy: {policy} | Audit ID: {audit_id}"
    )
    st.divider()

    st.subheader("Business Intelligence")

    b1, b2, b3, b4 = st.columns(4)

    with b1:
        st.metric(
            "Business Value",
            max(100 - score, 10)
        )

    with b2:
        st.metric(
            "Business Risk",
            score
        )

    with b3:
        st.metric(
            "Regulatory Impact",
            "High" if score >= 70 else "Medium"
        )

    with b4:
        st.metric(
            "Operational Complexity",
            "High" if score >= 60 else "Low"
        )

    # --------------------------------------------------
    # DECISION INTELLIGENCE
    # --------------------------------------------------

    st.divider()

    st.header("Decision Intelligence")

    left, right = st.columns([1, 1])
    # ---------------------------------------------
    # Risk Intelligence
    # ---------------------------------------------

    with left:

        st.subheader("Risk Intelligence")

        risk_types = result.get("risk_types", [])

        if isinstance(risk_types, str):
            risk_types = [risk_types]

        if risk_types:

            for risk in risk_types:

                st.write(f"• {risk}")

        else:

            st.info("No risk categories identified.")

        st.markdown("---")

        st.subheader("Policy Triggered")

        st.info(policy)

    # ---------------------------------------------
    # Business Impact
    # ---------------------------------------------

    with right:

        st.subheader("Business Impact Assessment")

        st.write(

            result.get(

                "impact",

                "No business impact available."

            )

        )

    # ---------------------------------------------
    # Opportunities
    # ---------------------------------------------

    st.divider()

    st.header("Opportunity Analysis")

    opportunities = result.get(

        "opportunities",

        []

    )

    if opportunities:

        for opportunity in opportunities:

            st.success(opportunity)

    else:

        st.info("No opportunities identified.")

    # ---------------------------------------------
    # Recommendations
    # ---------------------------------------------

    st.divider()

    st.header("Executive Recommendations")

    recommendations = result.get(

        "recommendations",

        []

    )

    if recommendations:

        for recommendation in recommendations:

            st.write(f"➡ {recommendation}")

    else:

        st.info("No recommendations available.")

# --------------------------------------------------
# GOVERNANCE WORKFLOW
# --------------------------------------------------

    st.divider()

    st.header("Governance Workflow")

    if audit_required:

        st.warning(
            "This decision requires governance approval before execution."
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Approve Decision",
                use_container_width=True
            ):

                st.session_state["governance"] = "APPROVED"

        with col2:

            if st.button(
                "Reject Decision",
                use_container_width=True
            ):

                st.session_state["governance"] = "REJECTED"

    else:

        st.success(
            "Eligible for Straight Through Processing (STP)"
        )

        if st.button(
            "Record Audit",
            use_container_width=True
        ):

            st.session_state["governance"] = "AUTO_APPROVED"

    # ---------------------------------------------
    # Governance Status
    # ---------------------------------------------

    if "governance" in st.session_state:

        state = st.session_state["governance"]

        if state == "APPROVED":

            st.success("Governance Approval Recorded")

        elif state == "REJECTED":

            st.error("Decision Rejected")

        elif state == "AUTO_APPROVED":

            st.info("Automatically Recorded")

    # --------------------------------------------------
    # ENTERPRISE AUDIT TRAIL
    # --------------------------------------------------

    st.divider()

    st.header("Enterprise Audit Trail")

    audit1, audit2 = st.columns(2)

    with audit1:

        st.markdown(f"**Audit ID**  \n`{audit_id}`")

        st.markdown(f"**Workflow**  \n`{workflow}`")

    with audit2:

        st.markdown(f"**Policy Triggered**  \n`{policy}`")

        st.markdown(f"**Audit Required**  \n`{audit_required}`")

    # --------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------

    st.divider()

    st.header("Executive Summary")

    summary = f"""
### Final Recommendation

**Decision:** {decision}

**Risk Score:** {score}/100

**Risk Level:** {risk_level}

**Workflow:** {workflow}

**Policy:** {policy}

**Audit Required:** {audit_required}
"""

    if decision == "APPROVE":

        st.success(summary)

    elif decision == "REVIEW":

        st.warning(summary)

    elif decision == "ESCALATE":

        st.warning(summary)

    else:

        st.error(summary)

    # --------------------------------------------------
    # FOOTER
    # --------------------------------------------------

    st.divider()

    st.caption(
        "Sentinel Enterprise Decision Intelligence Platform | Version 3.0 | Built with AI + Policy Intelligence"
    )
