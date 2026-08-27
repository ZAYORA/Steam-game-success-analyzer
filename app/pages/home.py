import streamlit as st
import pandas as pd
import json
import os

def load_dashboard_stats():
    """Loads stats dynamically with bulletproof pathing."""
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 1. Bulletproof CSV Locator
    csv_paths = [
        os.path.abspath(os.path.join(base_dir, '..', '..', 'data', 'steam_games_clustered.csv')),
    ]
    csv_path = next((p for p in csv_paths if os.path.exists(p)), None)

    # 2. Bulletproof Meta Locator
    meta_paths = [
        os.path.abspath(os.path.join(base_dir, '..', '..', 'model', 'metadata.json')),
    ]
    meta_path = next((p for p in meta_paths if os.path.exists(p)), None)

    # Default fallback stats
    stats = {
        "total_games": "124,146",
        "auc": "94.2%",
        "silhouette": "0.412",
        "features_used": "69" # Make sure this matches the key below
    }

    # Extract CSV Data
    if csv_path:
        try:
            df = pd.read_csv(csv_path)
            stats["total_games"] = f"{len(df):,}"
        except Exception:
            pass

    # Extract JSON Data
    if meta_path:
        try:
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                
                # ✅ THIS WAS THE MISSING LINE IN YOUR CODE ✅
                stats["features_used"] = str(meta.get('features_used', '14'))
                
                best_model = meta.get('best_model', 'Gradient Boosting')
                
                perf = meta.get('model_performance', {})
                if best_model in perf:
                    auc_val = perf[best_model].get('auc', 0.942)
                    stats["auc"] = f"{auc_val * 100:.2f}%"
                
                sil = meta.get('silhouette_score', 0.412)
                stats["silhouette"] = f"{sil:.4f}"
        except Exception as e:
            st.error(f"Error reading JSON: {e}")
    else:
        st.warning("⚠️ metadata.json tidak ditemukan di folder model/ Anda.")

    return stats

def show():
    # ── FETCH DYNAMIC STATS ──────────────────────────────────────
    stats = load_dashboard_stats()

    # ── HERO ────────────────────────────────────────────────────
    st.markdown("""
    <div style="padding: 2.5rem 0 1.5rem;">
        <div class="hero-subtitle">// STEAM GAME ANALYTICS PLATFORM</div>
        <div class="hero-title">Predicting Game<br>Success at Launch</div>
        <p class="hero-desc" style="margin-top:1rem;">
            Platform analitik berbasis <strong style="color:#0369a1">Data Mining</strong> untuk memprediksi
            tingkat keberhasilan game di Steam menggunakan kombinasi
            <strong style="color:#7e22ce">Random Forest Classification</strong> dan
            <strong style="color:#15803d">K-Means Clustering</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ── QUICK STATS (NOW DYNAMIC) ───────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Games", stats["total_games"], "Steam Dataset")
    with c2:
        st.metric("Model AUC", stats["auc"], "+2.1% vs baseline")
    with c3:
        st.metric("Silhouette Score", stats["silhouette"], "K=4 Optimal")
    with c4:
        # ✅ Make sure this asks for "features_used" instead of "features"
        st.metric("Features Used", stats["features_used"], "Launch-day only")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── PIPELINE OVERVIEW ───────────────────────────────────────
    st.markdown('<div class="section-title">🔬 Pipeline CRISP-DM</div>', unsafe_allow_html=True)

    stages = [
        ("01", "Business Understanding", "Identifikasi faktor sukses game Steam berdasarkan data penjualan & engagement", "#0369a1"),
        ("02", "Data Understanding",     "Eksplorasi dataset game Steam dengan fitur teknis dan pasar dari FronkonGames",       "#7e22ce"),
        ("03", "Data Preparation",       "Feature engineering: market impact score, engagement score, platform flags",   "#15803d"),
        ("04", "Modeling",               "Random Forest (best AUC) + K-Means Clustering (k=4 archetypes)",              "#b45309"),
        ("05", "Evaluation",             "Confusion matrix, ROC-AUC, Silhouette & Davies-Bouldin score",                "#b91c1c"),
        ("06", "Deployment",             "Streamlit web app dengan prediksi real-time & visualisasi interaktif",        "#0369a1"),
    ]

    cols = st.columns(3)
    for i, (num, title, desc, color) in enumerate(stages):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:1rem; min-height:140px;">
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem;
                            color:{color}; letter-spacing:0.1em; margin-bottom:0.5rem; font-weight:700;">STEP {num}</div>
                <div style="font-family:'Orbitron',monospace; font-weight:700;
                            font-size:0.82rem; color:#0f172a; margin-bottom:0.5rem;
                            letter-spacing:0.04em;">{title}</div>
                <div style="font-size:0.82rem; color:#475569; line-height:1.55;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── SUCCESS TIERS ────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏆 Success Tier System</div>', unsafe_allow_html=True)

    tiers = [
        ("💀", "Failure",         "< 0.20",    "Underpromising launch",       "tier-failure"),
        ("📦", "Moderate",        "0.20–0.40", "Below-average performance",   "tier-moderate"),
        ("✅", "Successful",      "0.40–0.60", "Solid commercial release",    "tier-successful"),
        ("🔥", "Hit",             "0.60–0.80", "Strong market performance",   "tier-hit"),
        ("💎", "Generational Hit","≥ 0.80",    "Top-tier iconic status",      "tier-gen"),
    ]

    cols = st.columns(5)
    for i, (icon, label, score_range, desc, cls) in enumerate(tiers):
        with cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:1.2rem 0.8rem;">
                <div style="font-size:1.8rem; margin-bottom:0.5rem;">{icon}</div>
                <div class="tier-badge {cls}" style="margin:0 auto 0.5rem;">{label}</div>
                <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem;
                            color:#475569; margin-bottom:0.4rem; font-weight:600;">{score_range}</div>
                <div style="font-size:0.75rem; color:#475569;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── TEAM ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">👥 Tim Pengembang — Kelompok 15 | KDD01 - DTMG1</div>', unsafe_allow_html=True)

    members = [
        ("D", "Daniel Evan Rusli",           "NIM: 24051214009", "SI 2024A, Sistem Informasi, UNESA"),
        ("A", "Azzahra Anggarista Yoan P.",  "NIM: 24051214032", "SI 2024A, Sistem Informasi, UNESA"),
        ("M", "Maria Elvaretta Cempaka Ayu", "NIM: 24051214033", "SI 2024A, Sistem Informasi, UNESA"),
    ]

    cols = st.columns(3)
    for i, (initial, name, nim, dept) in enumerate(members):
        with cols[i]:
            st.markdown(f"""
            <div class="member-card">
                <div class="member-avatar">{initial}</div>
                <div>
                    <div class="member-name">{name}</div>
                    <div class="member-nim">{nim}</div>
                    <div style="font-size:0.75rem; color:#475569; margin-top:2px;">{dept}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── CTA ──────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="text-align:center; padding:2rem;">
        <div style="font-family:'Orbitron',monospace; font-size:1.1rem; font-weight:700;
                    color:#0f172a; margin-bottom:0.5rem;">Ready to Analyze?</div>
        <div style="color:#475569; font-size:0.9rem; margin-bottom:1.2rem;">
            Masukkan parameter game Anda dan dapatkan prediksi tier keberhasilan secara instan.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀  Mulai Prediksi Sekarang", use_container_width=True):
            st.session_state["_nav_target"] = "prediction"
            st.rerun()