
W
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
