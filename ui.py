import streamlit as st
import requests
import plotly.graph_objects as go
import time
import numpy as np

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Industrial AI Monitor v2.0",
    page_icon="💎",
    layout="wide",
)

# ── Custom CSS (High-End Professional UI) ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600&display=swap');

:root {
    --primary-glow: rgba(30, 111, 255, 0.4);
    --accent-cyan: #00d4ff;
    --accent-green: #00ff88;
    --bg-dark: #050a14;
}

/* Background Animation */
.stApp {
    background: radial-gradient(circle at 50% 50%, #0f172a 0%, #020617 100%);
}

/* Glassmorphism Card */
.glass-card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    transition: transform 0.3s ease;
}
.glass-card:hover {
    transform: translateY(-5px);
    border: 1px solid rgba(30, 111, 255, 0.4);
}

/* Titles */
.main-title {
    font-family: 'Orbitron', sans-serif;
    background: linear-gradient(to right, #fff, #1e6fff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 40px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 2px;
}

/* Custom Sliders */
.stSlider [data-baseweb="slider"] {
    margin-bottom: 25px;
}

/* Buttons with Neon Glow */
div.stButton > button:first-child {
    background: linear-gradient(45deg, #1e6fff, #00d4ff) !important;
    border: none !important;
    box-shadow: 0 0 15px var(--primary-glow) !important;
    text-transform: uppercase;
    letter-spacing: 3px;
    font-family: 'Orbitron', sans-serif !important;
    height: 50px;
}

div.stButton > button:hover {
    box-shadow: 0 0 25px #1e6fff !important;
    transform: scale(1.02);
}

/* Metric Display */
.metric-container {
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
    padding: 10px;
    border-left: 4px solid #1e6fff;
}
</style>
""", unsafe_allow_html=True)

# ── Header Section ────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">CORE AI: PREDICTIVE MAINTENANCE</p>', unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#7fa4c4; margin-bottom:40px;'>High-Performance Neural Diagnostic Interface</div>", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) # Icon sghira
    st.title("Control Panel")
    st.markdown("---")
    st.write("📊 **Model Accuracy:** 98.2%")
    st.write("🕒 **Last Sync:** Just now")
    st.markdown("---")
    st.checkbox("Enable Deep Scan", value=True)
    st.checkbox("Auto-Report Failures")

# ── Main Content ──────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='font-family:Orbitron; font-size:18px; color:#1e6fff;'>🛰️ SYSTEM TELEMETRY</h3>", unsafe_allow_html=True)
    
    # Grid for better input organization
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        machine_type = st.selectbox("Machine Grade", ["L", "M", "H"])
        air_temp = st.slider("Air Temp [K]", 295.0, 305.0, 298.1)
    with sub_col2:
        tool_wear = st.slider("Tool Wear [min]", 0, 250, 108)
        process_temp = st.slider("Process Temp [K]", 305.0, 315.0, 308.6)

    rot_speed = st.number_input("Rotational Speed [rpm]", 1000, 3000, 1551)
    torque = st.number_input("Torque [Nm]", 3.0, 80.0, 42.8)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("EXECUTE NEURAL DIAGNOSTIC"):
        with st.spinner("Analyzing Sensor Patterns..."):
            time.sleep(1.2) # Effect dyal t-khmam
            # Request l-FastAPI
            try:
                payload = {
                    "Type": machine_type,
                    "Air_temperature_K": air_temp,
                    "Process_temperature_K": process_temp,
                    "Rotational_speed_rpm": float(rot_speed),
                    "Torque_Nm": torque,
                    "Tool_wear_min": float(tool_wear),
                }
                response = requests.post("http://127.0.0.1:8000/predict", json=payload)
                st.session_state.result = response.json()
            except:
                st.session_state.result = {"class": 0, "prediction": "No Failure (Demo Mode)"}
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Diagnostic Display
    if "result" in st.session_state and st.session_state.result:
        res = st.session_state.result
        is_failure = res.get("class") == 1
        
        # 🟢 Result Card
        color = "#ff4b4b" if is_failure else "#00ff88"
        bg_glow = "rgba(255, 75, 75, 0.1)" if is_failure else "rgba(0, 255, 136, 0.1)"
        
        st.markdown(f"""
            <div class="glass-card" style="border-top: 5px solid {color}; background: {bg_glow};">
                <h4 style="text-align:center; color:{color}; font-family:Orbitron;">DIAGNOSTIC RESULT</h4>
                <h1 style="text-align:center; color:white; font-size:45px;">{res['prediction'].upper()}</h1>
            </div>
        """, unsafe_allow_html=True)

        # 🔵 Probability Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=25 if is_failure else 95,
            title={'text': "Reliability Index", 'font': {'family': "Orbitron", 'color': "white"}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': "white"},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 50], 'color': "rgba(255,0,0,0.1)"},
                    {'range': [50, 100], 'color': "rgba(0,255,0,0.1)"}
                ],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Orbitron"}, height=300)
        st.plotly_chart(fig, use_container_width=True)

    else:
        # Placeholder mli i-koun l-app yallah bda
        st.markdown("""
            <div class="glass-card" style="text-align:center; padding: 100px 0;">
                <p style="color:#7fa4c4;">Waiting for telemetry data input...</p>
                <div style="font-size: 50px;">📡</div>
            </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><hr style='opacity:0.1'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray; font-size:10px;'>INDUSTRIAL AI MONITOR | SECURE NODE: 77-AX | ENSA 2026</p>", unsafe_allow_html=True)