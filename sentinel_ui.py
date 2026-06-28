import streamlit as st
from engine import analyze_decision

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Sentinel Enterprise Decision Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family:'Inter',sans-serif;
}

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.stApp{
background:#F4F7FB;
}

.block-container{
padding-top:2rem;
padding-bottom:2rem;
max-width:1500px;
}

/* HERO */

.hero{

background:linear-gradient(135deg,#0E4D92,#1C3D72);

padding:35px;

border-radius:18px;

color:white;

margin-bottom:30px;

box-shadow:0 10px 25px rgba(0,0,0,.15);

}

.hero h1{

font-size:42px;

margin-bottom:5px;

}

.hero p{

font-size:18px;

opacity:.9;

}

/* CARD */

.card{

background:white;

padding:20px;

border-radius:16px;

border:1px solid #E8EDF5;

box-shadow:0 4px 15px rgba(0,0,0,.05);

}

/* BUTTON */

.stButton>button{

background:#0E4D92;

color:white;

height:52px;

font-size:17px;

font-weight:600;

border-radius:12px;

border:none;

width:100%;

transition:.3s;

}

.stButton>button:hover{

background:#0A3564;

}

/* TEXT AREA */

textarea{

border-radius:12px !important;

}

/* SIDEBAR */

[data-testid="stSidebar"]{

background:#102542;

}

[data-testid="stSidebar"] *{

color:white;

}

/* KPI */

.metric-box{

background:white;

padding:20px;

border-radius:16px;

text-align:center;

box-shadow:0 5px 20px rgba(0,0,0,.05);

border:1px solid #EDF1F7;

}

/* MOBILE */

@media(max-width:768px){

.hero h1{

font-size:28px;

}

.hero p{

font-size:15px;

}

.block-container{

padding:1rem;

}

}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.title("🛡 Sentinel")

    st.caption("Enterprise AI Platform")

    st.divider()

    st.markdown("### Modules")

    st.markdown("🏠 Dashboard")

    st.markdown("🧠 AI Decision")

    st.markdown("📊 Risk Intelligence")

    st.markdown("⚖ Governance")

    st.markdown("📜 Audit Trail")

    st.markdown("📈 Analytics")

    st.divider()

    st.info(
        """
Version 4.0

Enterprise Edition

AI + Policy Intelligence
"""
    )

# ==========================================================
# HERO
# ==========================================================

st.markdown("""

<div class="hero">

<h1>🛡 Sentinel Enterprise Decision Intelligence</h1>

<p>

Enterprise AI • Governance • Policy Intelligence • Risk Intelligence

</p>

</div>

""", unsafe_allow_html=True)

# ==========================================================
# INPUT
# ==========================================================

left,right=st.columns([3,2])

with left:

    st.subheader("Decision Context")

    user_input=st.text_area(

        "Describe your business decision",

        height=260,

        placeholder="""
Examples

• Launch Loan Against Securities

• Increase LTV from 50% to 65%

• Launch AI Credit Underwriting

• Approve ₹50 Crore Investment

• Delete Customer Data

• Open Operations in UAE

• Launch Wealth Lending Platform

"""
    )

with right:

    st.subheader("Decision Information")

    decision_type=st.selectbox(

        "Decision Type",

        [

            "Business Decision",

            "Credit Decision",

            "Risk Decision",

            "Governance Decision",

            "Investment Decision",

            "AI Decision"

        ]

    )

    department=st.selectbox(

        "Department",

        [

            "Retail Banking",

            "Corporate Banking",

            "Risk",

            "Operations",

            "Technology",

            "Compliance"

        ]

    )

    priority=st.select_slider(

        "Priority",

        options=[

            "Low",

            "Medium",

            "High",

            "Critical"

        ],

        value="Medium"

    )

    analyze=st.button(

        "🚀 Analyze Decision",

        use_container_width=True,

        type="primary"

    )

# ==========================================================
# EXECUTION
# ==========================================================

if analyze:

    if not user_input.strip():

        st.warning("Please enter a business decision.")

        st.stop()

    with st.spinner("🧠 Sentinel AI is analysing your decision..."):

        st.session_state.result=analyze_decision(user_input)

# ==========================================================
# DASHBOARD START
# ==========================================================

if "result" in st.session_state:

    result=st.session_state.result

    if "error" in result:

        st.error(result["error"])

        st.stop()

    score=result.get("risk_score",0)

    risk_level=result.get("risk_level","N/A")

    decision=result.get("decision","REVIEW")

    workflow=result.get("workflow","N/A")

    policy=result.get("policy_triggered","N/A")

    audit_required=result.get("audit_required",False)

    audit_id=result.get("audit_id","N/A")

    if score>=80:

        confidence=95

    elif score>=60:

        confidence=91

    elif score>=40:

        confidence=87

    else:

        confidence=98

    # ==========================================================
    # EXECUTIVE DASHBOARD
    # ==========================================================

    st.markdown("## 📊 Executive Decision Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Risk Score",
            f"{score}/100"
        )

    with c2:
        st.metric(
            "Decision",
            decision
        )

    with c3:
        st.metric(
            "Workflow",
            workflow
        )

    with c4:
        st.metric(
            "AI Confidence",
            f"{confidence}%"
        )

    st.write("")

    # ==========================================================
    # DECISION STATUS
    # ==========================================================

    if decision == "APPROVE":

        st.success(
            "✅ Decision Approved"
        )

    elif decision == "REVIEW":

        st.warning(
            "🟡 Decision Requires Review"
        )

    elif decision == "ESCALATE":

        st.warning(
            "⚠ Escalate to Governance Committee"
        )

    else:

        st.error(
            "❌ Decision Rejected"
        )

    st.caption(
        f"Workflow • {workflow}    |    Policy • {policy}    |    Audit • {audit_id}"
    )

    st.divider()

    # ==========================================================
    # ENTERPRISE RISK DASHBOARD
    # ==========================================================

    st.subheader("Enterprise Risk Dashboard")

    st.progress(score / 100)

    r1, r2 = st.columns([3, 1])

    with r1:

        if score >= 80:

            st.error("Critical Enterprise Risk")

        elif score >= 60:

            st.warning("High Enterprise Risk")

        elif score >= 40:

            st.info("Medium Enterprise Risk")

        else:

            st.success("Low Enterprise Risk")

    with r2:

        st.metric(
            "Risk Level",
            risk_level
        )

    st.write("")

    # ==========================================================
    # BUSINESS METRICS
    # ==========================================================

    st.subheader("Business Intelligence")

    b1, b2, b3, b4 = st.columns(4)

    with b1:

        st.metric(
            "Business Value",
            f"{max(100-score,10)}%"
        )

    with b2:

        st.metric(
            "Business Risk",
            f"{score}%"
        )

    with b3:

        st.metric(
            "Regulatory",
            "High" if score >= 70 else "Medium"
        )

    with b4:

        st.metric(
            "Operational",
            "High" if score >= 60 else "Low"
        )

    st.divider()

    # ==========================================================
    # ENTERPRISE TABS
    # ==========================================================

    overview, risks, opportunities, recommendations = st.tabs(
        [
            "📋 Overview",
            "⚠ Risk Intelligence",
            "💡 Opportunities",
            "🎯 Recommendations"
        ]
    )

    # ==========================================================
    # OVERVIEW
    # ==========================================================

    with overview:

        left, right = st.columns([2, 1])

        with left:

            st.subheader("Business Impact")

            st.write(
                result.get(
                    "impact",
                    "No impact available."
                )
            )

        with right:

            st.metric(
                "Decision",
                decision
            )

            st.metric(
                "Risk",
                risk_level
            )

            st.metric(
                "Confidence",
                f"{confidence}%"
            )

    # ==========================================================
    # RISK TAB
    # ==========================================================

    with risks:

        st.subheader("Risk Categories")

        risk_types = result.get(
            "risk_types",
            []
        )

        if isinstance(risk_types, str):

            risk_types = [
                x.strip()
                for x in risk_types.split(",")
            ]

        if risk_types:

            for item in risk_types:

                st.warning(item)

        else:

            st.success(
                "No risks detected."
            )

        st.write("")

        st.info(
            f"Triggered Policy : {policy}"
        )

    # ==========================================================
    # OPPORTUNITIES
    # ==========================================================

    with opportunities:

        opps = result.get(
            "opportunities",
            []
        )

        if opps:

            for item in opps:

                st.success(item)

        else:

            st.info(
                "No opportunities identified."
            )

    # ==========================================================
    # RECOMMENDATIONS
    # ==========================================================

    with recommendations:

        recs = result.get(
            "recommendations",
            []
        )

        if recs:

            for item in recs:

                st.write(
                    f"➡ {item}"
                )

        else:

            st.info(
                "No recommendations available."
            )

    # ==========================================================
    # GOVERNANCE WORKFLOW
    # ==========================================================

    st.divider()

    st.header("⚖ Governance Workflow")

    g1, g2 = st.columns([2, 1])

    with g1:

        if audit_required:

            st.warning(
                "This decision requires Governance approval before execution."
            )

            a1, a2 = st.columns(2)

            with a1:

                if st.button(
                    "✅ Approve Decision",
                    use_container_width=True
                ):
                    st.session_state["governance"] = "APPROVED"

            with a2:

                if st.button(
                    "❌ Reject Decision",
                    use_container_width=True
                ):
                    st.session_state["governance"] = "REJECTED"

        else:

            st.success(
                "Eligible for Straight Through Processing (STP)"
            )

            if st.button(
                "📝 Record Audit",
                use_container_width=True
            ):
                st.session_state["governance"] = "AUTO_APPROVED"

    with g2:

        st.info(
            f"""
### Decision Summary

**Decision**

{decision}

**Workflow**

{workflow}

**Risk Level**

{risk_level}

**Audit Required**

{audit_required}
"""
        )

    # ==========================================================
    # GOVERNANCE STATUS
    # ==========================================================

    if "governance" in st.session_state:

        state = st.session_state["governance"]

        if state == "APPROVED":

            st.success("✅ Governance Approval Recorded")

        elif state == "REJECTED":

            st.error("❌ Decision Rejected")

        elif state == "AUTO_APPROVED":

            st.info("📝 Audit Successfully Recorded")

    # ==========================================================
    # AUDIT TRAIL
    # ==========================================================

    st.divider()

    st.header("📜 Enterprise Audit Trail")

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        st.metric("Audit ID", audit_id)

    with a2:
        st.metric("Workflow", workflow)

    with a3:
        st.metric("Policy", policy)

    with a4:
        st.metric(
            "Audit",
            "Required" if audit_required else "Not Required"
        )

    st.write("")

    st.code(
f"""
Audit ID          : {audit_id}

Workflow          : {workflow}

Triggered Policy  : {policy}

Risk Level        : {risk_level}

Decision          : {decision}

Confidence        : {confidence}%

Audit Required    : {audit_required}
"""
    )

    # ==========================================================
    # EXECUTIVE SUMMARY
    # ==========================================================

    st.divider()

    st.header("📋 Executive Summary")

    summary = f"""

Decision            : {decision}

Risk Score          : {score}/100

Risk Level          : {risk_level}

Workflow            : {workflow}

Policy Triggered    : {policy}

Audit Required      : {audit_required}

AI Confidence       : {confidence}%

"""

    if decision == "APPROVE":

        st.success(summary)

    elif decision == "REVIEW":

        st.warning(summary)

    elif decision == "ESCALATE":

        st.warning(summary)

    else:

        st.error(summary)

    # ==========================================================
    # ENTERPRISE INSIGHTS
    # ==========================================================

    st.divider()

    st.header("📊 Enterprise Insights")

    i1, i2, i3 = st.columns(3)

    with i1:

        st.metric(
            "Automation",
            "92%"
        )

        st.caption("Potential Straight Through Processing")

    with i2:

        st.metric(
            "Risk Reduction",
            f"{max(100-score,15)}%"
        )

        st.caption("Estimated Risk Mitigation")

    with i3:

        st.metric(
            "Decision Confidence",
            f"{confidence}%"
        )

        st.caption("AI Assessment Confidence")

    st.divider()

    # ==========================================================
    # FOOTER
    # ==========================================================

    st.markdown(
        """
<hr>

<div style='text-align:center;
padding:20px;
color:gray;'>

<h4>🛡 Sentinel Enterprise Decision Intelligence</h4>

AI • Policy Intelligence • Governance • Enterprise Risk

<br>

Version 4.0 Enterprise Edition

</div>
""",
        unsafe_allow_html=True
    )
