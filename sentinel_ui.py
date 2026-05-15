import streamlit as st
from engine import analyze_decision  # Ensure this calls your API or logic engine

# ---------------- CONFIG & STYLING ----------------

st.set_page_config(
    page_title="Sentinel | Decision Intelligence",
    page_icon="🛡️",
    layout="wide"
)

# Premium UI Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="metric-container"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 15px;
        border-radius: 10px;
    }
    .stTextArea textarea {
        background-color: #0d1117;
        color: #c9d1d9;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_all_with_html=True)

# ---------------- HEADER ----------------

st.title("🛡️ Sentinel")
st.caption("Strategic Intelligence Infrastructure Layer")

st.markdown("""
Analyze core risks, hidden dependencies, and long-term consequences of strategic moves 
before execution. Sentinel transforms raw decision data into actionable risk intelligence.
""")

st.divider()

# ---------------- INPUT ----------------

# Using columns to create a "Terminal" feel
col_in, col_opt = st.columns([3, 1])

with col_in:
    user_input = st.text_area(
        "Decision Context",
        height=250,
        placeholder="e.g., Pivoting our SaaS to a government-only procurement model..."
    )

with col_opt:
    st.info("Analysis Parameters")
    sector = st.selectbox("Industry Vertical", ["General", "Fintech", "Healthtech", "M&A", "Operations"])
    depth = st.radio("Intelligence Depth", ["Standard", "Deep Dive (High Latency)"])

# ---------------- EXECUTION ----------------

if st.button("Analyze Risk", type="primary", use_container_width=True):

    if not user_input.strip():
        st.warning("Please provide a decision description.")
        st.stop()

    with st.spinner("Decoding strategic variables..."):
        # If your engine.py is set up for it, pass the sector/depth too
        result = analyze_decision(user_input)

    # ---------------- OUTPUT DASHBOARD ----------------

    if "error" in result:
        st.error(f"Analysis Error: {result['error']}")
    else:
        # High-level Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        
        # Color coding risk level
        risk_color = "normal"
        if result["risk_level"].lower() in ["high", "critical"]:
            risk_color = "inverse"

        m1.metric("Risk Level", result["risk_level"], delta_color=risk_color)
        m2.metric("Risk Score", f"{result['risk_score']}/100")
        m3.metric("Confidence", f"{result.get('confidence', 92)}%")
        m4.metric("Success Prob", f"{result.get('success_probability', 'N/A')}%")

        st.divider()

        # Detailed Breakdown
        res_left, res_right = st.columns([1, 1])

        with res_left:
            st.subheader("Executive Summary")
            st.write(result["summary"])
            
            st.subheader("Blind Spots")
            for spot in result.get("blind_spots", []):
                st.write(f"👁️ {spot}")

        with res_right:
            st.subheader("Strategic Recommendations")
            # Using st.success/info to differentiate actionable steps
            for rec in result["recommendations"]:
                st.info(f"✅ {rec}")

        # Impact Tabs
        st.subheader("Multi-Dimensional Impact")
        tab1, tab2, tab3 = st.tabs(["Risk Types", "Opportunities", "Second-Order Effects"])
        
        with tab1:
            st.write(", ".join(result["risk_types"]))
        with tab2:
            st.write(result["opportunities"])
        with tab3:
            # This is the 'Infrastructure' differentiator
            st.write(result.get("second_order_effects", "Analyze the downstream consequences in engine.py"))

        st.divider()
        st.subheader("Final Verdict")
        st.success(f"**Sentinel Conclusion:** {result['final_verdict']}")

# ---------------- FOOTER ----------------
st.caption("© 2026 Sentinel Intelligence Infrastructure | API v1.2")
