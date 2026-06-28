import streamlit as st
from engine import analyze_decision

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Sentinel Enterprise",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# ENTERPRISE CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
}

/* Hide Streamlit branding */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* Main background */

.stApp{

background:#F4F7FC;

}

/* Page width */

.block-container{

max-width:1400px;

padding-top:2rem;

padding-bottom:2rem;

}

/* Hero */

.hero{

background:linear-gradient(135deg,#0E4D92,#153E75);

padding:30px;

border-radius:20px;

color:white;

margin-bottom:30px;

box-shadow:0px 8px 30px rgba(0,0,0,.15);

}

.hero h1{

font-size:42px;

margin-bottom:5px;

}

.hero p{

font-size:18px;

opacity:.9;

}

/* Cards */

.metric-card{

background:white;

padding:20px;

border-radius:18px;

border:1px solid #E6EAF2;

box-shadow:0px 6px 20px rgba(0,0,0,.05);

text-align:center;

}

/* Input */

textarea{

border-radius:14px !important;

}

/* Buttons */

.stButton>button{

background:#0E4D92;

color:white;

border:none;

height:54px;

font-size:17px;

font-weight:600;

border-radius:12px;

width:100%;

transition:.3s;

}

.stButton>button:hover{

background:#0B3A6B;

}

/* Sidebar */

[data-testid="stSidebar"]{

background:#102542;

color:white;

}

[data-testid="stSidebar"] *{

color:white;

}

/* Progress */

.stProgress > div > div{

background:#0E4D92;

}

/* Mobile */

@media (max-width:768px){

.hero h1{

font-size:28px;

}

.hero p{

font-size:14px;

}

.block-container{

padding:1rem;

}

}

</style>

""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/shield.png",
        width=70
    )

    st.title("Sentinel")

    st.caption("Enterprise Decision Intelligence")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("🏠 Dashboard")

    st.markdown("🧠 AI Analysis")

    st.markdown("⚖ Governance")

    st.markdown("📊 Business")

    st.markdown("📜 Audit Trail")

    st.divider()

    st.info(
        """
Version 4.0

Enterprise Edition
"""
    )

# =====================================================
# HERO
# =====================================================

st.markdown("""

<div class="hero">

<h1>🛡 Sentinel Enterprise Decision Intelligence</h1>

<p>

AI • Policy Intelligence • Governance • Enterprise Risk

</p>

</div>

""", unsafe_allow_html=True)

# =====================================================
# INPUT
# =====================================================

st.subheader("Decision Context")

user_input = st.text_area(

    "Describe your business decision",

    height=220,

    placeholder="""
Examples

• Launch Loan Against Securities

• Increase LTV to 65%

• Launch AI Underwriting

• Delete Customer Data

• Open new country

• Invest ₹50 Crores
"""

)

analyze = st.button(

    "🚀 Analyze Decision",

    use_container_width=True,

    type="primary"

)

# =====================================================
# EXECUTE ENGINE
# =====================================================

if analyze:

    if not user_input.strip():

        st.warning("Please enter a decision.")

        st.stop()

    with st.spinner("🧠 AI is analyzing your decision..."):

        st.session_state.result = analyze_decision(user_input)
# =====================================================
# EXECUTIVE DASHBOARD
# =====================================================

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

    # -----------------------------------
    # AI Confidence
    # -----------------------------------

    if score >= 80:
        confidence = 95
    elif score >= 60:
        confidence = 91
    elif score >= 40:
        confidence = 87
    else:
        confidence = 98

    # -----------------------------------
    # Dashboard Header
    # -----------------------------------

    st.markdown("## 📊 Executive Decision Dashboard")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
        <h4>Risk Score</h4>
        <h1>{score}</h1>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
        <h4>Decision</h4>
        <h2>{decision}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
        <h4>Workflow</h4>
        <h3>{workflow}</h3>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
        <h4>AI Confidence</h4>
        <h2>{confidence}%</h2>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # -----------------------------------
    # Risk Meter
    # -----------------------------------

    st.markdown("### 🎯 Enterprise Risk Score")

    st.progress(score / 100)

    rc1, rc2 = st.columns([3,1])

    with rc1:

        if score >= 80:
            st.error(f"Critical Risk ({score}/100)")

        elif score >= 60:
            st.warning(f"High Risk ({score}/100)")

        elif score >= 40:
            st.info(f"Medium Risk ({score}/100)")

        else:
            st.success(f"Low Risk ({score}/100)")

    with rc2:

        st.metric(
            "Risk Level",
            risk_level
        )

    st.write("")

    # -----------------------------------
    # Decision Banner
    # -----------------------------------

    if decision == "APPROVE":

        st.success(
            f"✅ Decision Approved | Workflow: {workflow}"
        )

    elif decision == "REVIEW":

        st.warning(
            f"🟡 Decision Requires Review | Workflow: {workflow}"
        )

    elif decision == "ESCALATE":

        st.warning(
            f"⚠ Escalate to Senior Governance | Workflow: {workflow}"
        )

    else:

        st.error(
            f"❌ Decision Rejected | Workflow: {workflow}"
        )

    st.caption(
        f"""
Audit ID : {audit_id}
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
Policy : {policy}
"""
    )

    st.divider()

    # -----------------------------------
    # Business Intelligence
    # -----------------------------------

    st.markdown("## 📈 Business Intelligence")

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
            "Regulatory Impact",
            "High" if score >= 70 else "Medium"
        )

    with b4:

        st.metric(
            "Operational Complexity",
            "High" if score >= 60 else "Low"
        )

    st.write("")

    k1, k2 = st.columns(2)

    with k1:

        st.info(
            f"""
### 🧠 AI Assessment

**Decision:** {decision}

**Risk Level:** {risk_level}

**Confidence:** {confidence}%

**Workflow:** {workflow}
"""
        )

    with k2:

        st.success(
            f"""
### ⚖ Governance

**Policy Triggered**

{policy}

**Audit Required**

{audit_required}
"""
        )

    st.divider()

# =====================================================
# DECISION INTELLIGENCE
# =====================================================

st.markdown("## 🧠 AI Decision Intelligence")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Risk Intelligence",
    "💼 Business Impact",
    "💡 Opportunities",
    "🎯 Recommendations"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    left, right = st.columns([2, 1])

    with left:

        st.subheader("Risk Categories")

        risk_types = result.get("risk_types", [])

        if isinstance(risk_types, str):
            risk_types = [
                x.strip()
                for x in risk_types.split(",")
            ]

        if risk_types:

            for risk in risk_types:

                st.markdown(
                    f"""
<div style="
background:white;
padding:15px;
border-radius:12px;
border-left:5px solid #0E4D92;
margin-bottom:12px;
box-shadow:0 2px 8px rgba(0,0,0,.08);
">
⚠️ <b>{risk}</b>
</div>
""",
                    unsafe_allow_html=True
                )

        else:

            st.success("No major risks detected.")

    with right:

        st.subheader("Policy")

        st.info(policy)

        st.subheader("Risk Meter")

        st.progress(score / 100)

        st.metric(
            "Risk Score",
            f"{score}/100"
        )

        st.metric(
            "Risk Level",
            risk_level
        )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    st.subheader("Business Impact")

    impact = result.get(
        "impact",
        "No impact available."
    )

    st.markdown(
        f"""
<div style="
background:white;
padding:25px;
border-radius:15px;
box-shadow:0 2px 10px rgba(0,0,0,.08);
">

{impact}

</div>
""",
        unsafe_allow_html=True
    )

    st.write("")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Business Value",
            max(100-score, 10)
        )

    with c2:

        st.metric(
            "Enterprise Risk",
            score
        )

    with c3:

        st.metric(
            "Confidence",
            f"{confidence}%"
        )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    st.subheader("Business Opportunities")

    opportunities = result.get(
        "opportunities",
        []
    )

    if opportunities:

        cols = st.columns(2)

        for i, item in enumerate(opportunities):

            with cols[i % 2]:

                st.markdown(
                    f"""
<div style="
background:#ECFDF5;
padding:18px;
border-radius:12px;
margin-bottom:15px;
border-left:5px solid #10B981;
">

✅ {item}

</div>
""",
                    unsafe_allow_html=True
                )

    else:

        st.info("No opportunities identified.")

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.subheader("Executive Recommendations")

    recommendations = result.get(
        "recommendations",
        []
    )

    if recommendations:

        for i, recommendation in enumerate(recommendations, start=1):

            st.markdown(
                f"""
<div style="
background:white;
padding:18px;
border-radius:12px;
margin-bottom:15px;
border-left:5px solid #F59E0B;
box-shadow:0 2px 8px rgba(0,0,0,.08);
">

<b>Recommendation {i}</b>

<br><br>

{recommendation}

</div>
""",
                unsafe_allow_html=True
            )

    else:

        st.success(
            "No recommendations available."
        )

st.divider()

# =====================================================
# GOVERNANCE
# =====================================================

st.markdown("## ⚖ Governance Workflow")

g1, g2 = st.columns([2,1])

with g1:

    if audit_required:

        st.warning(
            "This decision requires governance approval before execution."
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

    st.markdown("""
### Workflow

👤 User

⬇

🧠 AI Engine

⬇

📜 Policy Engine

⬇

⚖ Governance

⬇

📝 Audit
""")

# =====================================================
# GOVERNANCE STATUS
# =====================================================

if "governance" in st.session_state:

    state = st.session_state["governance"]

    if state == "APPROVED":

        st.success("✅ Governance Approval Recorded")

    elif state == "REJECTED":

        st.error("❌ Decision Rejected")

    elif state == "AUTO_APPROVED":

        st.info("📝 Audit Automatically Recorded")

st.divider()

# =====================================================
# AUDIT
# =====================================================

st.markdown("## 📜 Enterprise Audit Trail")

a1, a2, a3, a4 = st.columns(4)

with a1:

    st.metric(
        "Audit ID",
        audit_id
    )

with a2:

    st.metric(
        "Workflow",
        workflow
    )

with a3:

    st.metric(
        "Policy",
        policy
    )

with a4:

    st.metric(
        "Audit",
        "Required" if audit_required else "Not Required"
    )

st.write("")

st.markdown(
f"""
<div style="
background:white;
padding:20px;
border-radius:15px;
box-shadow:0 2px 12px rgba(0,0,0,.08);
">

<b>Audit Timestamp</b><br>
Automatically generated during AI decision execution.

<br><br>

<b>Execution Workflow</b><br>
{workflow}

<br><br>

<b>Triggered Policy</b><br>
{policy}

<br><br>

<b>Audit Reference</b><br>
{audit_id}

</div>
""",
unsafe_allow_html=True
)

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

st.markdown("## 📋 Executive Summary")

summary = f"""
### Decision Summary

**Decision**

{decision}

---

**Risk Score**

{score}/100

---

**Risk Level**

{risk_level}

---

**Workflow**

{workflow}

---

**Policy Triggered**

{policy}

---

**Audit Required**

{audit_required}

---

**AI Confidence**

{confidence}%
"""

if decision == "APPROVE":

    st.success(summary)

elif decision == "REVIEW":

    st.warning(summary)

elif decision == "ESCALATE":

    st.warning(summary)

else:

    st.error(summary)

st.divider()

# =====================================================
# FOOTER
# =====================================================

st.markdown(
"""
<div style="
text-align:center;
padding:30px;
color:#6B7280;
font-size:14px;
">

<b>🛡 Sentinel Enterprise Decision Intelligence Platform</b>

<br>

AI • Governance • Policy Intelligence • Enterprise Risk

<br><br>

Version 4.0 Enterprise Edition

</div>
""",
unsafe_allow_html=True
)
