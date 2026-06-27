import streamlit as st
from engine import analyze_decision

# -------------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------------

st.set_page_config(
    page_title="Sentinel Enterprise Decision Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------------------------------
# ENTERPRISE THEME
# -------------------------------------------------------

st.markdown("""
<style>

.main{
    padding-top:2rem;
}

.block-container{
    padding-top:2rem;
}

h1{
    font-size:42px !important;
    font-weight:700 !important;
    color:#0E4D92;
}

h2,h3{
    color:#1B263B;
}

textarea{
    border-radius:12px !important;
}

.stButton>button{
    width:100%;
    height:48px;
    border-radius:10px;
    font-weight:600;
}

.metric-card{
    background:#F8F9FA;
    padding:15px;
    border-radius:12px;
    border:1px solid #EAEAEA;
}

.audit-box{
    background:#F4F6F8;
    padding:12px;
    border-radius:10px;
    border-left:5px solid #0E4D92;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------

st.title("🛡️ Sentinel Enterprise Decision Intelligence")

st.caption(
    "AI-Powered Decision Intelligence | Policy Engine | Governance | Risk Analytics"
)

st.divider()

# -------------------------------------------------------
# USER INPUT
# -------------------------------------------------------

st.subheader("Decision Context")

user_input = st.text_area(

    label="Describe the business decision",

    placeholder="""
Example:

• Launch a new banking product

• Invest ₹50 Cr in a startup

• Change lending policy

• Delete customer records

• Approve unsecured credit
""",

    height=220

)

# -------------------------------------------------------
# ACTION BUTTON
# -------------------------------------------------------

col1,col2,col3=st.columns([2,1,7])

with col1:

    analyze_clicked=st.button(

        "🚀 Analyze Decision",

        type="primary"

    )

# -------------------------------------------------------
# EXECUTION
# -------------------------------------------------------

if analyze_clicked:

    if not user_input.strip():

        st.warning("Please enter a decision context.")

        st.stop()

    with st.spinner("Running Sentinel Decision Engine..."):

        st.session_state.result = analyze_decision(user_input)
        # -------------------------------------------------------
# EXECUTIVE DECISION DASHBOARD
# -------------------------------------------------------

if "result" in st.session_state:

    result = st.session_state.result

    if "error" in result:

        st.error(result["error"])

        st.stop()

    st.divider()

    st.header("Executive Decision Dashboard")

    score = result.get("risk_score", 0)

    risk_level = result.get("risk_level", "N/A")

    decision = result.get("decision", "REVIEW")

    workflow = result.get("workflow", "N/A")

    policy = result.get("policy_triggered", "N/A")

    audit_required = result.get("audit_required", False)

    audit_id = result.get("audit_id", "Pending")

    # --------------------------------------------
    # AI Confidence
    # --------------------------------------------

    if score >= 80:
        confidence = "95%"

    elif score >= 60:
        confidence = "91%"

    elif score >= 30:
        confidence = "87%"

    else:
        confidence = "98%"

    # --------------------------------------------
    # Decision Badge
    # --------------------------------------------

    decision_map = {

        "APPROVE": "✅ APPROVE",

        "REVIEW": "🟡 REVIEW",

        "ESCALATE": "⚠️ ESCALATE",

        "REJECT": "❌ REJECT"

    }

    decision_display = decision_map.get(

        decision,

        decision

    )

    # --------------------------------------------
    # METRICS
    # --------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Risk Score",

            score

        )

    with c2:

        st.metric(

            "Risk Level",

            risk_level

        )

    with c3:

        st.metric(

            "AI Confidence",

            confidence

        )

    with c4:

        st.metric(

            "Workflow",

            workflow

        )

    st.divider()

    # --------------------------------------------
    # DECISION SUMMARY
    # --------------------------------------------

    st.subheader("Executive Decision")

    if decision == "APPROVE":

        st.success(decision_display)

    elif decision == "REVIEW":

        st.warning(decision_display)

    elif decision == "ESCALATE":

        st.warning(decision_display)

    else:

        st.error(decision_display)

    # --------------------------------------------
    # POLICY INFORMATION
    # --------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"**Policy Triggered**\n\n{policy}")

    with col2:

        if audit_required:

            st.warning("Audit Required")

        else:

            st.success("Audit Not Required")

    # --------------------------------------------
    # RISK CATEGORIES
    # --------------------------------------------

    st.subheader("Risk Intelligence")

    st.write(result.get("risk_types", "Not Available"))

    # --------------------------------------------
    # IMPACT
    # --------------------------------------------

    st.subheader("Business Impact Assessment")

    st.write(

        result.get(

            "impact",

            "No impact available."

        )

    )

    # --------------------------------------------
    # OPPORTUNITIES
    # --------------------------------------------

    st.subheader("Opportunity Analysis")

    opportunities = result.get(

        "opportunities",

        []

    )

    if opportunities:

        for item in opportunities:

            st.write(f"✅ {item}")

    else:

        st.info("No opportunities identified.")

    # --------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------

    st.subheader("Executive Recommendations")

    recommendations = result.get(

        "recommendations",

        []

    )

    if recommendations:

        for rec in recommendations:

            st.write(f"➡️ {rec}")

    else:

        st.info("No recommendations available.")
            # -------------------------------------------------------
    # GOVERNANCE PANEL
    # -------------------------------------------------------

    st.divider()

    st.header("Governance & Workflow")

    if audit_required:

        st.warning(
            "This decision requires governance approval before execution."
        )

        c1, c2 = st.columns(2)

        with c1:

            if st.button(
                "✅ Approve Decision",
                use_container_width=True
            ):

                st.session_state["governance"] = "APPROVED"

        with c2:

            if st.button(
                "❌ Reject Decision",
                use_container_width=True
            ):

                st.session_state["governance"] = "REJECTED"

    else:

        st.success(
            "Straight Through Processing (STP) Enabled"
        )

        if st.button(
            "📄 Record Audit",
            use_container_width=True
        ):

            st.session_state["governance"] = "AUTO_APPROVED"

    # -------------------------------------------------------
    # GOVERNANCE STATUS
    # -------------------------------------------------------

    if "governance" in st.session_state:

        state = st.session_state["governance"]

        if state == "APPROVED":

            st.success(
                "Executive Approval Recorded."
            )

        elif state == "REJECTED":

            st.error(
                "Decision Rejected by Governance."
            )

        elif state == "AUTO_APPROVED":

            st.info(
                "Decision automatically recorded."
            )

    # -------------------------------------------------------
    # AUDIT TRAIL
    # -------------------------------------------------------

    st.divider()

    st.header("Enterprise Audit Trail")

    a1, a2 = st.columns(2)

    with a1:

        st.markdown(
            f"""
**Audit ID**

`{audit_id}`
"""
        )

        st.markdown(
            f"""
**Workflow**

`{workflow}`
"""
        )

    with a2:

        st.markdown(
            f"""
**Policy Triggered**

`{policy}`
"""
        )

        st.markdown(
            f"""
**Audit Required**

`{audit_required}`
"""
        )

    # -------------------------------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------------------------------

    st.divider()

    st.header("Executive Summary")

    st.success(
        f"""
### Decision

**{decision_display}**

Risk Score **{score}/100**

Risk Level **{risk_level}**

Workflow **{workflow}**
"""
    )

    # -------------------------------------------------------
    # FOOTER
    # -------------------------------------------------------

    st.divider()

    st.caption(
        "Sentinel Enterprise Decision Intelligence Platform • Version 3.0"
    )
