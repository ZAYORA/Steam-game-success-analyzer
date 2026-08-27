import streamlit as st

st.set_page_config(
    page_title="Steam Game Success Analyzer",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# =====================
# MASTER DESIGN SYSTEM
# =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Sembunyikan auto-page navigation Streamlit */
[data-testid="stSidebarNav"] {
    display: none !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}

:root {
    --neon-blue:    #0ea5e9;
    --neon-green:   #22c55e;
    --neon-purple:  #a855f7;
    --neon-red:     #ef4444;
    --neon-gold:    #f59e0b;
    --bg-main:      #f0f4ff;
    --bg-panel:     #e8eeff;
    --bg-card:      #ffffff;
    --bg-glass:     rgba(255,255,255,0.85);
    --border-dim:   rgba(14,165,233,0.2);
    --border-glow:  rgba(14,165,233,0.6);
    --text-primary: #0f172a;
    --text-dim:     #334155;
    --text-muted:   #64748b;
    --font-display: 'Orbitron', monospace;
    --font-body:    'Space Grotesk', sans-serif;
    --font-code:    'JetBrains Mono', monospace;
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"] {
    font-family: var(--font-body);
    background-color: var(--bg-main) !important;
    color: var(--text-primary) !important;
}

.main .block-container {
    padding: 1.5rem 2.5rem 3rem;
    max-width: 1400px;
    background: var(--bg-main);
}

/* ── ANIMATED BACKGROUND ── */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 20% 0%, rgba(14,165,233,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(168,85,247,0.08) 0%, transparent 60%),
        var(--bg-main);
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e1b4b 0%, #172554 50%, #0c1a3d 100%) !important;
    border-right: 2px solid rgba(14,165,233,0.3) !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, #0ea5e9, #a855f7, transparent);
}

/* Semua teks di sidebar */
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* ── SIDEBAR RADIO ── */
[data-testid="stRadio"] > div { gap: 0.25rem !important; }
[data-testid="stRadio"] label {
    display: flex !important;
    align-items: center !important;
    gap: 0.75rem !important;
    padding: 0.65rem 1.1rem !important;
    border-radius: 8px !important;
    border: 1px solid transparent !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    font-size: 0.92rem !important;
    color: #cbd5e1 !important;
    font-family: var(--font-body) !important;
    letter-spacing: 0.02em !important;
    font-weight: 500 !important;
}
[data-testid="stRadio"] label:hover {
    background: rgba(14,165,233,0.15) !important;
    border-color: rgba(14,165,233,0.4) !important;
    color: #7dd3fc !important;
}
[data-testid="stRadio"] [aria-checked="true"] + label,
[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background: rgba(14,165,233,0.2) !important;
    border-color: #0ea5e9 !important;
    color: #7dd3fc !important;
    box-shadow: 0 0 12px rgba(14,165,233,0.2) inset !important;
}
[data-testid="stRadio"] [type="radio"] { display: none !important; }

PLOTLY_THEME = {
    "template": "plotly_white",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "font": dict(color="#0f172a", family="Inter, sans-serif", size=12),
    "margin": dict(l=20, r=20, t=40, b=20)
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 12px !important;
    padding: 1.2rem 1.4rem !important;
    position: relative !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(14,165,233,0.08) !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border-glow) !important;
    box-shadow: 0 4px 20px rgba(14,165,233,0.15) !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple));
}
[data-testid="stMetricLabel"] { color: #475569 !important; font-size: 0.8rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; font-weight: 600 !important; }
[data-testid="stMetricValue"] { color: #0369a1 !important; font-family: var(--font-display) !important; font-size: 1.8rem !important; }
[data-testid="stMetricDelta"] { color: #16a34a !important; font-size: 0.78rem !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--font-display) !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    background: linear-gradient(135deg, #0ea5e9, #a855f7) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.6rem !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 4px 15px rgba(14,165,233,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(14,165,233,0.45) !important;
    color: #ffffff !important;
}

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input,
[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1.5px solid #cbd5e1 !important;
    border-radius: 8px !important;
    color: #0f172a !important;
    font-family: var(--font-code) !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: var(--neon-blue) !important;
    box-shadow: 0 0 0 3px rgba(14,165,233,0.15) !important;
}
.stTextInput label, .stNumberInput label, .stSelectbox label, .stSlider label,
.stMultiSelect label, .stToggle label {
    color: #334155 !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
}
/* Toggle / checkbox text */
[data-testid="stToggle"] span {
    color: #1e293b !important;
    font-weight: 600 !important;
}

/* ── SLIDERS ── */
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--neon-blue) !important;
    box-shadow: 0 0 8px rgba(14,165,233,0.5) !important;
}

/* ── DATAFRAMES / TABLES ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid var(--border-dim); box-shadow: 0 2px 12px rgba(0,0,0,0.06); }
[data-testid="stDataFrame"] thead th {
    background: rgba(14,165,233,0.1) !important;
    color: #0369a1 !important;
    font-family: var(--font-display) !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 700 !important;
}

/* ── TABS ── */
[data-baseweb="tab-list"] {
    background: #ffffff !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border-dim) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
}
[data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 7px !important;
    color: #475569 !important;
    font-family: var(--font-body) !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.2s !important;
}
[data-baseweb="tab"]:hover { color: #0ea5e9 !important; background: rgba(14,165,233,0.08) !important; }
[aria-selected="true"][data-baseweb="tab"] {
    background: linear-gradient(135deg, rgba(14,165,233,0.15), rgba(168,85,247,0.15)) !important;
    color: #0369a1 !important;
    box-shadow: 0 2px 8px rgba(14,165,233,0.2) !important;
    font-weight: 700 !important;
}

/* ── EXPANDERS ── */
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid var(--border-dim) !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}
[data-testid="stExpander"] summary {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* ── ALERTS ── */
[data-testid="stInfo"] { background: rgba(14,165,233,0.08) !important; border: 1px solid rgba(14,165,233,0.3) !important; border-radius: 8px !important; color: #0c4a6e !important; }
[data-testid="stSuccess"] { background: rgba(34,197,94,0.08) !important; border: 1px solid rgba(34,197,94,0.3) !important; border-radius: 8px !important; color: #14532d !important; }
[data-testid="stWarning"] { background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.3) !important; border-radius: 8px !important; color: #78350f !important; }

/* ── TYPOGRAPHY ── */
.hero-title {
    font-family: var(--font-display);
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #0369a1 0%, #7c3aed 50%, #be185d 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    letter-spacing: -0.01em;
}

.hero-subtitle {
    font-family: var(--font-code);
    font-size: 0.88rem;
    color: #0ea5e9;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    font-weight: 600;
}

.hero-desc {
    color: #334155;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 680px;
}

/* Section headers */
.section-title {
    font-family: var(--font-display);
    font-size: 1rem;
    font-weight: 700;
    color: #0369a1;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, rgba(14,165,233,0.5), transparent);
}

/* Glass card */
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 14px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, box-shadow 0.3s;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    color: #0f172a;
}
.glass-card:hover {
    border-color: rgba(14,165,233,0.5);
    box-shadow: 0 8px 30px rgba(14,165,233,0.12);
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, rgba(14,165,233,0.6), transparent);
}
/* Text inside glass-card */
.glass-card, .glass-card * {
    color: #0f172a;
}

/* Tier badges */
.tier-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: var(--font-code);
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.tier-failure    { background: rgba(239,68,68,0.12);   color: #b91c1c; border: 1px solid rgba(239,68,68,0.4); }
.tier-moderate   { background: rgba(245,158,11,0.12);  color: #b45309; border: 1px solid rgba(245,158,11,0.4); }
.tier-successful { background: rgba(34,197,94,0.12);   color: #15803d; border: 1px solid rgba(34,197,94,0.4); }
.tier-hit        { background: rgba(14,165,233,0.12);  color: #0369a1; border: 1px solid rgba(14,165,233,0.4); }
.tier-gen        { background: rgba(168,85,247,0.12);  color: #7e22ce; border: 1px solid rgba(168,85,247,0.4); }

/* Member card */
.member-card {
    background: #ffffff;
    border: 1px solid rgba(14,165,233,0.2);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.25s, box-shadow 0.25s;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.member-card:hover {
    border-color: rgba(14,165,233,0.5);
    box-shadow: 0 6px 20px rgba(14,165,233,0.12);
}
.member-avatar {
    width: 44px; height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #0ea5e9, #a855f7);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display);
    font-weight: 700; font-size: 1rem;
    color: #ffffff;
    flex-shrink: 0;
}
.member-name { font-family: var(--font-body); font-weight: 700; font-size: 1rem; color: #0f172a; }
.member-nim  { font-family: var(--font-code); font-size: 0.78rem; color: #0369a1; margin-top: 2px; font-weight: 600; }

/* Sidebar brand */
.sidebar-brand {
    padding: 1.5rem 1.2rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 0.8rem;
}
.sidebar-logo {
    font-size: 2.5rem;
    line-height: 1;
    filter: drop-shadow(0 0 8px #0ea5e9);
}
.sidebar-app-name {
    font-family: var(--font-display);
    font-size: 1.05rem;
    font-weight: 700;
    color: #f1f5f9 !important;
    letter-spacing: 0.05em;
    margin-top: 0.4rem;
}
.sidebar-tagline {
    font-family: var(--font-code);
    font-size: 0.7rem;
    color: #94a3b8 !important;
    letter-spacing: 0.08em;
    margin-top: 2px;
}

/* Prediction result card */
.pred-result {
    background: #ffffff;
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.pred-result-label {
    font-family: var(--font-display);
    font-size: 2rem;
    font-weight: 900;
    margin: 0.5rem 0;
}

/* Markdown text override */
.stMarkdown p, .stMarkdown li, .stMarkdown span {
    color: #1e293b !important;
}
p { color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# =====================
# SIDEBAR
# =====================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-logo">🎮</div>
        <div class="sidebar-app-name">STEAM ANALYZER</div>
        <div class="sidebar-tagline">// DATA MINING UAS</div>
    </div>
    """, unsafe_allow_html=True)

    pages = {
        "🏠  Home":              "home",
        "📊  Dataset Overview":  "dataset",
        "👾  Prediction":        "prediction",
        "📈  Visualization":     "visualization",
        "ℹ️  About":             "about"
    }

    # Handle nav redirect dari tombol
    if "_nav_target" in st.session_state:
        target = st.session_state.pop("_nav_target")
        default_idx = list(pages.values()).index(target) if target in pages.values() else 0
    else:
        default_idx = 0

    selected = st.radio("nav", list(pages.keys()), index=default_idx, label_visibility="collapsed")
    page = pages[selected]

    st.markdown("""
    <hr style="border-color:rgba(255,255,255,0.1); margin:1rem 0;">
    <div style="padding:0 0.2rem">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.68rem; color:#94a3b8; line-height:2.2;">
            FRAMEWORK &nbsp;→&nbsp; CRISP-DM<br>
            CLASSIFICATION → GRADIENT BOOSTING<br>
            CLUSTERING &nbsp;&nbsp;&nbsp;&nbsp;→ K-MEANS<br>
            DATASET &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ STEAM GAMES<br>
            KELAS &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→ KDD01 - DTMG1
        </div>
    </div>
    <hr style="border-color:rgba(255,255,255,0.1); margin:1rem 0;">
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#64748b; text-align:center; letter-spacing:0.05em;">
        KELOMPOK 15 &nbsp;•&nbsp; INFORMATIKA<br>
        UNESA © 2025
    </div>
    """, unsafe_allow_html=True)

# =====================
# PAGE ROUTING
# =====================
if page == "home":
    import pages.home as home_page
    home_page.show()
elif page == "dataset":
    import pages.dataset as dataset_page
    dataset_page.show()
elif page == "prediction":
    import pages.prediction as prediction_page
    prediction_page.show()
elif page == "visualization":
    import pages.visualization as viz_page
    viz_page.show()
elif page == "about":
    import pages.about as about_page
    about_page.show()
