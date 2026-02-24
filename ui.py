import streamlit as st
import requests
import plotly.graph_objects as go
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Industrial AI Monitor",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* Root */
:root {
    --navy: #0d1b2a;
    --navy-mid: #112240;
    --navy-card: #172a45;
    --blue-accent: #1e6fff;
    --cyan: #00c8ff;
    --green: #00e676;
    --text-primary: #e8f4fd;
    --text-muted: #7fa4c4;
    --border: rgba(30,111,255,0.25);
}

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #e8edf2 !important;
    color: var(--text-primary);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #0a1628 100%) !important;
    border-right: 1px solid var(--border);
    min-width: 220px !important;
    max-width: 220px !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .sidebar-badge {
    background: rgba(0,200,255,0.12);
    border: 1px solid var(--cyan);
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 11px;
    color: var(--cyan) !important;
    font-weight: 600;
    letter-spacing: 1px;
}

/* Cards */
.card {
    background: linear-gradient(145deg, #1a2f4a, #142238);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 28px 24px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 20px;
}
.card-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-bottom: 20px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 10px;
}

/* Sliders */
[data-testid="stSlider"] > div > div > div {
    background: rgba(30,111,255,0.3) !important;
}
[data-testid="stSlider"] > div > div > div > div {
    background: var(--blue-accent) !important;
    border: 2px solid #fff !important;
    box-shadow: 0 0 8px rgba(30,111,255,0.8) !important;
}
[data-testid="stSlider"] label { color: var(--text-muted) !important; font-size: 13px !important; }

/* Select box */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* Button */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--blue-accent), #0050d0) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    padding: 14px 0 !important;
    width: 100% !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 20px rgba(30,111,255,0.5) !important;
}
[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 28px rgba(30,111,255,0.7) !important;
}

/* Metric */
.metric-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}
.metric-label { font-size: 12px; color: var(--text-muted); }
.metric-value { font-size: 12px; font-weight: 600; color: var(--cyan); }

/* Status badge */
.status-live {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
}
.status-dot {
    width: 7px; height: 7px;
    background: var(--green);
    border-radius: 50%;
    animation: pulse 1.5s infinite;
}
@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(0,230,118,0.5); }
    50% { box-shadow: 0 0 0 5px rgba(0,230,118,0); }
}

/* Nav items */
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background 0.15s;
    margin-bottom: 4px;
}
.nav-item:hover, .nav-item.active {
    background: rgba(30,111,255,0.15);
    color: #fff !important;
}
.nav-item.active { border-left: 3px solid var(--blue-accent); }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--navy); }
::-webkit-scrollbar-thumb { background: var(--blue-accent); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 24px 0;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
            <span style="font-size:22px;">⚙️</span>
            <div>
                <div style="font-family:'Rajdhani',sans-serif;font-size:16px;font-weight:700;
                            letter-spacing:1px;line-height:1.1;">INDUSTRIAL<br>AI MONITOR</div>
            </div>
        </div>
        <div style="font-size:11px;color:#7fa4c4;margin-bottom:4px;">
            <span class="status-dot" style="display:inline-block;width:7px;height:7px;
                  background:#00e676;border-radius:50%;margin-right:5px;"></span>
            STATUS: LIVE
        </div>
        <div style="font-size:11px;color:#7fa4c4;">UPTIME: 99.8%</div>
        <hr style="border-color:rgba(30,111,255,0.2);margin:18px 0 16px 0;">
        <div class="nav-item active">🏠 &nbsp; Dashboard</div>
        <div class="nav-item">📋 &nbsp; History</div>
        <div class="nav-item">⚙️ &nbsp; Settings</div>
    </div>
    """, unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "health_score" not in st.session_state:
    st.session_state.health_score = 85

# ── Layout: 2 columns ─────────────────────────────────────────────────────────
col_inputs, col_results = st.columns([1.1, 1], gap="large")

# ── LEFT: Sensor Inputs ───────────────────────────────────────────────────────
with col_inputs:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚡ Sensor Inputs</div>', unsafe_allow_html=True)

    machine_type = st.selectbox(
        "Machine Type",
        options=["L", "M", "H"],
        index=0,
        help="L = Low, M = Medium, H = High grade machine"
    )

    air_temp = st.slider(
        "Air Temperature [K]",
        min_value=295.0, max_value=305.0, value=298.1, step=0.1,
        format="%.1f K"
    )

    process_temp = st.slider(
        "Process Temperature [K]",
        min_value=305.0, max_value=315.0, value=308.6, step=0.1,
        format="%.1f K"
    )

    rot_speed = st.slider(
        "Rotational Speed [rpm]",
        min_value=1000, max_value=3000, value=1551, step=10,
        format="%d rpm"
    )

    torque = st.slider(
        "Torque [Nm]",
        min_value=3.0, max_value=80.0, value=42.8, step=0.1,
        format="%.1f Nm"
    )

    tool_wear = st.slider(
        "Tool Wear [min]",
        min_value=0, max_value=250, value=108, step=1,
        format="%d min"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("▶  RUN DIAGNOSTIC"):
        with st.spinner("Running diagnostic..."):
            time.sleep(0.6)
            try:
                payload = {
                    "Type": machine_type,
                    "Air_temperature_K": air_temp,
                    "Process_temperature_K": process_temp,
                    "Rotational_speed_rpm": float(rot_speed),
                    "Torque_Nm": torque,
                    "Tool_wear_min": float(tool_wear),
                }
                response = requests.post(
                    "http://127.0.0.1:8000/predict",
                    json=payload,
                    timeout=5
                )
                data = response.json()
                st.session_state.result = data
                # Update health score based on prediction
                st.session_state.health_score = 25 if data["class"] == 1 else 85
            except requests.exceptions.ConnectionError:
                st.session_state.result = {"error": "Cannot connect to API at http://127.0.0.1:8000"}
            except Exception as e:
                st.session_state.result = {"error": str(e)}

    st.markdown('</div>', unsafe_allow_html=True)

# ── RIGHT: Health Score + Feature Importance ──────────────────────────────────
with col_results:

    # Health Score Gauge
    score = st.session_state.health_score
    result = st.session_state.result

    if result and "error" in result:
        st.error(f"❌ API Error: {result['error']}")
        st.info("Make sure your FastAPI server is running: `uvicorn main:app --reload`")

    # Determine gauge color and status
    if result and result.get("class") == 1:
        gauge_color = "#ff4444"
        gauge_border = "#ff4444"
        status_text = "⚠️ FAILURE DETECTED"
        status_color = "#ff4444"
        score = 25
    else:
        gauge_color = "#00e676"
        gauge_border = "#00e676"
        status_text = "SAFE / STABLE"
        status_color = "#00e676"
        score = 85

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "suffix": "%",
            "font": {"size": 42, "color": "white", "family": "Rajdhani"},
        },
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 1,
                "tickcolor": "rgba(255,255,255,0.2)",
                "tickfont": {"color": "rgba(255,255,255,0.3)", "size": 9},
            },
            "bar": {"color": gauge_color, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(255,68,68,0.15)"},
                {"range": [40, 70], "color": "rgba(255,193,7,0.1)"},
                {"range": [70, 100], "color": "rgba(0,230,118,0.1)"},
            ],
            "threshold": {
                "line": {"color": gauge_color, "width": 3},
                "thickness": 0.8,
                "value": score,
            },
        },
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=240,
        margin=dict(l=20, r=20, t=20, b=10),
        font={"color": "white"},
    )

    st.markdown(f"""
    <div class="card" style="border-color:{gauge_border};
         box-shadow: 0 0 24px rgba(0,230,118,0.15);">
        <div class="card-title">🎯 Health Score</div>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
        <div style="text-align:center;font-family:'Rajdhani',sans-serif;
                    font-size:20px;font-weight:700;letter-spacing:3px;
                    color:{status_color};margin-top:-10px;margin-bottom:12px;">
            {status_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Feature Importance
    power_val = torque * rot_speed / 1000
    temp_diff_val = process_temp - air_temp
    torque_norm = min(torque / 80, 1.0)
    power_norm = min(power_val / 150, 1.0)
    temp_norm = min(temp_diff_val / 15, 1.0)

    fig_bar = go.Figure()
    features = ["Torque", "Power", "Temp Diff"]
    values = [torque_norm, power_norm, temp_norm]
    colors = ["#1e6fff", "#00c8ff", "#00e676"]

    for i, (feat, val, col) in enumerate(zip(features, values, colors)):
        fig_bar.add_trace(go.Bar(
            y=[feat],
            x=[val],
            orientation='h',
            marker=dict(color=col, line=dict(width=0)),
            width=0.55,
            showlegend=False,
        ))

    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=160,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(
            range=[0, 1.05],
            showgrid=False, showticklabels=False, zeroline=False,
        ),
        yaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(color="#7fa4c4", size=12, family="Inter"),
        ),
        barmode='overlay',
    )

    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Feature Importance</div>
    """, unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;font-size:11px;color:rgba(100,140,180,0.5);
            margin-top:10px;letter-spacing:1px;">
    ENSA Data Engineering Project 2026
</div>
""", unsafe_allow_html=True)