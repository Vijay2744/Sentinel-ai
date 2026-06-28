import streamlit as st
from engine import analyze_decision

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Sentinel Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# ENTERPRISE STYLING
# --------------------------------------------------

st.markdown("""
<style>

html,body,[class*="css"]{
    font-family:Segoe UI, sans-serif;
}

.main .block-container{
    max-width:1350px;
    padding-top:1.2rem;
    padding-bottom:2rem;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.stApp{
    background:#F5F7FB;
}

.hero{

background:linear-gradient(135deg,#0E4D92,#1E3A8A);

padding:30px;

border-radius:18px;

color:white;

margin-bottom:25px;

}

.hero h1{

margin:0;

font-size:40px;

}

.hero p{

margin-top:10px;

opacity:.9;

font-size:17px;

}

.stButton>button{

width:100%;

height:52px;

border-radius:12px;

font-weight:600;

font-size:16px;

}

textarea{

border-radius:12px !important;

}

[data-testid="stMetricValue"]{

font-size:32px;

}

.metric-card{

background:white;

padding:20px;

border-radius:15px;

border:1px solid #E7EAF0;

box-shadow:0 4px 14px rgba(0,0,0,.05);

}

@media(max-width:768px){

.hero h1{

font-size:28px;

}

.hero p{

font-size:14px;

}

.main .block-container{

padding-top:1rem;

}

}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------

st.markdown("""

<div class="hero">

<h1>🛡 Sentinel Enterprise</h1>

<p>

Decision Intelligence Platform

</p>

<p>

AI • Governance • Policy Intelligence • Enterprise Risk

</p>

</div>

""", unsafe_allow_html=True)

# --------------------------------------------------
# INPUT
# --------------------------------------------------

left,right=st.columns([4,1])

with left:

    st.subheader("Decision Context")

    user_input=st.text_area(

        "",

        height=180,

        placeholder="""
Examples

• Launch Loan Against Securities for NRIs

• Increase LTV from 50% to 65%

• Approve ₹50 Crore Investment

• Delete Customer Data

• Launch AI Credit Underwriting

• Enter New Market

"""
    )

with right:

    st.subheader("")

    st.write("")

    st.write("")

    analyze=st.button(

        "🚀 Analyze Decision",

        type="primary",

        use_container_width=True

    )

# --------------------------------------------------
# EXECUTE ENGINE
# --------------------------------------------------

if analyze:

    if not user_input.strip():

        st.warning("Please enter a business decision.")

        st.stop()

    with st.spinner("🧠 Sentinel AI is analysing the request..."):

        st.session_state.result=analyze_decision(user_input)

# --------------------------------------------------
# EXECUTIVE DECISION DASHBOARD
# --------------------------------------------------

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

        confidence="95%"

    elif score>=60:

        confidence="91%"

    elif score>=40:

        confidence="87%"

    else:

        confidence="98%"
    # ---------------------------------------------
    # EXECUTIVE DASHBOARD
    # ---------------------------------------------

    decision_map = {
        "APPROVE": ("🟢", "#10B981"),
        "REVIEW": ("🟡", "#F59E0B"),
        "ESCALATE": ("🟠", "#F97316"),
        "REJECT": ("🔴", "#EF4444")
    }

    icon, color = decision_map.get(
        decision,
        ("⚪", "#6B7280")
    )

    st.markdown("## 📊 Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Risk Score",
            f"{score}/100"
        )

    with c2:
        st.metric(
            "Risk Level",
            risk_level
        )

    with c3:
        st.metric(
            "Workflow",
            workflow
        )

    with c4:
        st.metric(
            "AI Confidence",
            confidence
        )

    st.write("")

    st.markdown(
        f"""
<div style="
background:white;
border-left:8px solid {color};
padding:18px;
border-radius:12px;
box-shadow:0 2px 10px rgba(0,0,0,.08);
margin-bottom:20px;
">

<h3 style="margin:0;">
{icon} {decision}
</h3>

<p style="margin-top:8px;color:#555;">
Workflow : <b>{workflow}</b>

&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;

Policy : <b>{policy}</b>

&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;

Audit : <b>{audit_id}</b>

</p>

</div>
""",
        unsafe_allow_html=True
    )

    # ---------------------------------------------
    # BUSINESS OVERVIEW
    # ---------------------------------------------

    b1, b2, b3, b4 = st.columns(4)

    with b1:

        st.metric(
            "Business Value",
            max(100-score,10)
        )

    with b2:

        st.metric(
            "Business Risk",
            score
        )

    with b3:

        st.metric(
            "Regulatory",
            "High" if score>=70 else "Medium"
        )

    with b4:

        st.metric(
            "Complexity",
            "High" if score>=60 else "Low"
        )

    st.divider()

    # ---------------------------------------------
    # ENTERPRISE TABS
    # ---------------------------------------------

    overview, risks, opportunities_tab, recommendations_tab = st.tabs([
        "📋 Overview",
        "⚠ Risk Intelligence",
        "💡 Opportunities",
        "🎯 Recommendations"
    ])

    # ---------------------------------------------
    # OVERVIEW
    # ---------------------------------------------

    with overview:

        left,right=st.columns([2,1])

        with left:

            st.subheader("Business Impact")

            st.write(
                result.get(
                    "impact",
                    "No business impact available."
                )
            )

        with right:

            st.info(f"""
**Risk Level**

{risk_level}

---

**Workflow**

{workflow}

---

**Confidence**

{confidence}
""")

    # ---------------------------------------------
    # RISK
    # ---------------------------------------------

    with risks:

        risk_types=result.get("risk_types",[])

        if isinstance(risk_types,str):

            risk_types=[x.strip() for x in risk_types.split(",")]

        if risk_types:

            for item in risk_types:

                st.warning(item)

        else:

            st.success("No major risks detected.")

        st.write("")

        st.info(f"Triggered Policy : {policy}")

    # ---------------------------------------------
    # OPPORTUNITIES
    # ---------------------------------------------

    with opportunities_tab:

        opportunities=result.get("opportunities",[])

        if opportunities:

            for item in opportunities:

                st.success(item)

        else:

            st.info("No opportunities identified.")

    # ---------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------

    with recommendations_tab:

        recommendations=result.get("recommendations",[])

        if recommendations:

            for item in recommendations:

                st.write(f"➡ {item}")

        else:

            st.info("No recommendations available.")
    # ---------------------------------------------
    # EXECUTIVE DASHBOARD
    # ---------------------------------------------

    decision_map = {
        "APPROVE": ("🟢", "#10B981"),
        "REVIEW": ("🟡", "#F59E0B"),
        "ESCALATE": ("🟠", "#F97316"),
        "REJECT": ("🔴", "#EF4444")
    }

    icon, color = decision_map.get(
        decision,
        ("⚪", "#6B7280")
    )

    st.markdown("## 📊 Executive Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Risk Score",
            f"{score}/100"
        )

    with c2:
        st.metric(
            "Risk Level",
            risk_level
        )

    with c3:
        st.metric(
            "Workflow",
            workflow
        )

    with c4:
        st.metric(
            "AI Confidence",
            confidence
        )

    st.write("")

    st.markdown(
        f"""
<div style="
background:white;
border-left:8px solid {color};
padding:18px;
border-radius:12px;
box-shadow:0 2px 10px rgba(0,0,0,.08);
margin-bottom:20px;
">

<h3 style="margin:0;">
{icon} {decision}
</h3>

<p style="margin-top:8px;color:#555;">
Workflow : <b>{workflow}</b>

&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;

Policy : <b>{policy}</b>

&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;

Audit : <b>{audit_id}</b>

</p>

</div>
""",
        unsafe_allow_html=True
    )

    # ---------------------------------------------
    # BUSINESS OVERVIEW
    # ---------------------------------------------

    b1, b2, b3, b4 = st.columns(4)

    with b1:

        st.metric(
            "Business Value",
            max(100-score,10)
        )

    with b2:

        st.metric(
            "Business Risk",
            score
        )

    with b3:

        st.metric(
            "Regulatory",
            "High" if score>=70 else "Medium"
        )

    with b4:

        st.metric(
            "Complexity",
            "High" if score>=60 else "Low"
        )

    st.divider()

    # ---------------------------------------------
    # ENTERPRISE TABS
    # ---------------------------------------------

    overview, risks, opportunities_tab, recommendations_tab = st.tabs([
        "📋 Overview",
        "⚠ Risk Intelligence",
        "💡 Opportunities",
        "🎯 Recommendations"
    ])

    # ---------------------------------------------
    # OVERVIEW
    # ---------------------------------------------

    with overview:

        left,right=st.columns([2,1])

        with left:

            st.subheader("Business Impact")

            st.write(
                result.get(
                    "impact",
                    "No business impact available."
                )
            )

        with right:

            st.info(f"""
**Risk Level**

{risk_level}

---

**Workflow**

{workflow}

---

**Confidence**

{confidence}
""")

    # ---------------------------------------------
    # RISK
    # ---------------------------------------------

    with risks:

        risk_types=result.get("risk_types",[])

        if isinstance(risk_types,str):

            risk_types=[x.strip() for x in risk_types.split(",")]

        if risk_types:

            for item in risk_types:

                st.warning(item)

        else:

            st.success("No major risks detected.")

        st.write("")

        st.info(f"Triggered Policy : {policy}")

    # ---------------------------------------------
    # OPPORTUNITIES
    # ---------------------------------------------

    with opportunities_tab:

        opportunities=result.get("opportunities",[])

        if opportunities:

            for item in opportunities:

                st.success(item)

        else:

            st.info("No opportunities identified.")

    # ---------------------------------------------
    # RECOMMENDATIONS
    # ---------------------------------------------

    with recommendations_tab:

        recommendations=result.get("recommendations",[])

        if recommendations:

            for item in recommendations:

                st.write(f"➡ {item}")

        else:

            st.info("No recommendations available.")
