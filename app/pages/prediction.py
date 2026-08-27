import streamlit as st
import numpy as np
import joblib
import os
from datetime import datetime

# ── Tier config ────────────────────────────────────────────────
TIER_CONFIG = {
    "Top-Tier Market Fit":    {"icon": "💎", "color": "#bf5fff", "desc": "Sangat kompetitif. Berada di persentil teratas dengan DNA fitur yang sangat dioptimalkan."},
    "Highly Competitive":     {"icon": "🔥", "color": "#00d4ff", "desc": "Daya saing kuat. Fitur sangat sejalan dengan tren audiens Steam modern."},
    "Above Average":          {"icon": "✅", "color": "#39ff14", "desc": "Lebih menjanjikan dari rata-rata rilis Steam. Memiliki pondasi yang solid."},
    "Average Competitor":     {"icon": "📦", "color": "#ffd700", "desc": "Berada di tengah lautan Steam. Akan membutuhkan marketing niche yang sangat spesifik."},
    "High Risk / Niche":      {"icon": "⚠️", "color": "#ff4757", "desc": "Sangat berisiko. Menghadapi jalan yang sangat berat untuk menonjol di pasar saat ini."},
}

# ── Median harga per genre — from EDA on Steam dataset (n=124,146) ──
GENRE_MEDIAN_PRICE = {
    'Action':               2.99,
    'Adventure':            2.99,
    'Casual':               1.99,
    'Indie':                2.49,
    'RPG':                  3.74,
    'Simulation':           2.99,
    'Strategy':             2.99,
    'Sports':               2.99,
    'Racing':               2.90,
    'Nudity':               1.99,
    'Gore':                 1.99,
    'Violent':              2.99,
    'Sexual Content':       1.99,
    'Massively Multiplayer': 2.39,  # median is $0 (mostly F2P) — fallback to overall median
}
DEFAULT_MEDIAN_PRICE = 2.39  # overall dataset median

Q3_ACHIEVEMENTS = 19.0
BEST_MONTHS     = [10, 11, 12, 3, 4]

TOP_GENRES = [
    'Action', 'Adventure', 'Casual', 'Indie',
    'RPG', 'Simulation', 'Strategy',
    'Sports', 'Racing',
    'Nudity', 'Gore', 'Violent', 'Sexual Content',
    'Massively Multiplayer',
]

# ── Mature content genres — shown with a disclaimer in UI ──
MATURE_GENRES = {'Nudity', 'Gore', 'Violent', 'Sexual Content'}

def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'model', 'prediction_model.pkl'))

    if os.path.exists(model_path):
        obj = joblib.load(model_path)
        if isinstance(obj, dict):
            model = obj.get('model') or obj.get('classifier') or obj.get('gb_model') or list(obj.values())[0]
            return model, True
        return obj, True
    return None, False

def get_genre_price_benchmark(genres):
    """Weighted average median price based on selected genres."""
    if not genres:
        return DEFAULT_MEDIAN_PRICE
    prices = [GENRE_MEDIAN_PRICE.get(g, DEFAULT_MEDIAN_PRICE) for g in genres]
    return sum(prices) / len(prices)

def show():
    st.markdown("""
    <div style="padding:2rem 0 1rem">
        <div class="hero-subtitle">// DECISION SUPPORT SYSTEM</div>
        <div class="hero-title" style="font-size:2rem;">Steam Launch Competitiveness</div>
        <p class="hero-desc" style="margin-top:0.6rem; font-size:0.9rem;">
            Masukkan rancangan fitur game Anda. Model AI kami membandingkan DNA game Anda dengan 124,000+ rilis historis untuk memberikan <strong>Skor Daya Saing (1-10)</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    model, model_loaded = load_model()
    current_year = datetime.now().year

    st.markdown("<br>", unsafe_allow_html=True)

    # ── INPUT FORM ───────────────────────────────────────────────
    left, right = st.columns([3, 2], gap="large")

    with left:
        st.markdown('<div class="section-title">⚙️ Parameter Game</div>', unsafe_allow_html=True)

        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                is_free = st.toggle("Free to Play", value=False)
                price = 0.0 if is_free else st.number_input("Harga (USD)", min_value=0.0, max_value=299.0, value=9.99, step=0.99)
            with c2:
                achievements = st.number_input("Jumlah Achievements", min_value=0, max_value=5000, value=25, step=5)

        c1, c2 = st.columns(2)
        with c1:
            windows = st.toggle("Windows", value=True)
        with c2:
            mac = st.toggle("macOS", value=False)
        linux = st.toggle("Linux / SteamOS", value=False)
        platform_count = int(windows) + int(mac) + int(linux)

        release_month = st.select_slider(
            "Bulan Rilis Target",
            options=list(range(1, 13)),
            value=10,
            format_func=lambda m: ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][m-1]
        )

        release_year = st.slider(
            "Tahun Rilis Target",
            min_value=current_year,
            max_value=current_year + 5,
            value=current_year + 1
        )

        genres = st.multiselect(
            "Genre Utama (Wajib)",
            options=TOP_GENRES,
            default=["Action", "Indie"],
            help="Pilih 1-4 genre yang paling mendeskripsikan core gameplay Anda. Data-driven dari 124k+ game Steam."
        )
        genre_count = len(genres)

        # ── Mature content notice ──
        selected_mature = [g for g in genres if g in MATURE_GENRES]
        if selected_mature:
            st.markdown(f"""
            <div style="background:rgba(255,71,87,0.07); border:1px solid rgba(255,71,87,0.3);
            border-radius:8px; padding:0.6rem 1rem; font-size:0.8rem; color:#ff4757; margin-top:0.5rem;">
            ⚠️ Genre mature terdeteksi ({', '.join(selected_mature)}). 
            Steam mewajibkan age gate & content descriptor untuk kategori ini.
            Pastikan game Anda sudah melalui proses review konten Steam.
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-title">📊 Input Summary</div>', unsafe_allow_html=True)

        price_benchmark = get_genre_price_benchmark(genres)

        st.markdown(f"""<div class="glass-card">
<table style="width:100%; font-size:0.83rem; border-collapse:collapse;">
<tr><td style="color:#475569; padding:5px 0;">Harga</td>
<td style="color:#0369a1; text-align:right; font-family:'JetBrains Mono',monospace;">{"FREE" if is_free else f"${price:.2f}"}</td></tr>
<tr><td style="color:#475569; padding:5px 0;">Achievements</td>
<td style="color:#0f172a; text-align:right; font-family:'JetBrains Mono',monospace;">{achievements}</td></tr>
<tr><td style="color:#475569; padding:5px 0;">Platforms</td>
<td style="color:#0f172a; text-align:right; font-family:'JetBrains Mono',monospace;">{platform_count}</td></tr>
<tr><td style="color:#475569; padding:5px 0;">Genre</td>
<td style="color:#0f172a; text-align:right; font-size:0.75rem;">{", ".join(genres) if genres else "—"}</td></tr>
<tr><td style="color:#475569; padding:5px 0;">Target Rilis</td>
<td style="color:#0f172a; text-align:right; font-family:'JetBrains Mono',monospace;">{["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][release_month-1]} {release_year}</td></tr>
<tr><td style="color:#475569; padding:5px 0; font-size:0.75rem;">Benchmark Harga Genre</td>
<td style="color:#8892a4; text-align:right; font-family:'JetBrains Mono',monospace; font-size:0.75rem;">${price_benchmark:.2f} avg median</td></tr>
</table>
</div>""", unsafe_allow_html=True)

        season_tip = ""
        if release_month in [10, 11, 12]:
            season_tip = "🎄 Q4 Holiday Season — Volume pemain & diskon tertinggi."
        elif release_month in [6, 7, 8]:
            season_tip = "☀️ Summer Sale period — Traffic organik tinggi."
        elif release_month in [2, 3]:
            season_tip = "🌸 Spring window — Jendela sepi kompetisi AAA."

        if season_tip:
            st.markdown(f"""<div style="background:rgba(14,165,233,0.07); border:1px solid rgba(14,165,233,0.25);
border-radius:8px; padding:0.75rem 1rem; font-size:0.82rem; color:#0369a1; margin-top:0.8rem;">
{season_tip}
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn = st.columns([2, 1, 2])[1]
    with col_btn:
        predict_btn = st.button("⚡  KALKULASI SKOR (1-10)", use_container_width=True)

    # ── RESULT ───────────────────────────────────────────────────
    if predict_btn:
        if len(genres) == 0:
            st.error("⚠️ Peringatan: Harap pilih setidaknya satu 'Genre Utama' sebelum melakukan evaluasi.")
            st.stop()

        if not model_loaded:
            st.error("⚠️ Peringatan: Model prediction_model.pkl tidak ditemukan. Pastikan file berada di folder /model.")
            st.stop()

        # ── Build feature vector — must match training feature_cols exactly ──
        features = {
                    "price":          price,
                    "is_free":        int(is_free),
                    "achievements":   achievements,
                    "platform_count": platform_count,
                    "release_year":   release_year,
                    "release_month":  release_month,
                    "genre_count":    genre_count,
                }
        for g in TOP_GENRES:
            features[f"genre_{g}"] = 1 if g in genres else 0

        # Combo features — must match training exactly
        GENRE_COMBOS = [
            ('RPG',    'Massively Multiplayer'),
            ('Action', 'Massively Multiplayer'),
            ('Sports', 'Racing'),
        ]
        for g1, g2 in GENRE_COMBOS:
            features[f"combo_{g1}_{g2}"] = (
                features[f"genre_{g1}"] * features[f"genre_{g2}"]
            )

        combo_cols = [f"combo_{g1}_{g2}" for g1, g2 in GENRE_COMBOS]

        feature_cols = [
            'price', 'is_free', 'achievements', 'platform_count',
            'release_year', 'release_month', 'genre_count'
        ] + [f'genre_{g}' for g in TOP_GENRES] + combo_cols

        X = np.array([[features[c] for c in feature_cols]])
        proba = model.predict_proba(X)[0]

        # ── Base score from model probabilities ──
        if hasattr(model, 'classes_') and len(model.classes_) > 2:
            prob_dict = dict(zip(model.classes_, proba))
            base_score = (
                prob_dict.get('Failure', 0)          * 1.5 +
                prob_dict.get('Moderate', 0)         * 3.0 +
                prob_dict.get('Successful', 0)       * 4.5 +
                prob_dict.get('Hit', 0)              * 6.0 +
                prob_dict.get('Generational Hit', 0) * 7.5
            )
        else:
            base_score = 1.0 + (proba[1] * 6.5)

        price_benchmark = get_genre_price_benchmark(genres)

        # ── Penalties ──
        penalties = 0.0
        if price > 100:
            penalties -= 5.0
        elif price > 50:
            penalties -= 3.0
        elif price > price_benchmark * 4:
            penalties -= 1.5
        if achievements == 0:
            penalties -= 1.0
        if genre_count > 4:
            penalties -= 1.0  # identity crisis

        raw_score = base_score + penalties

        # ── Bonuses ──
        if is_free or price <= price_benchmark * 1.5:
            raw_score += 1.0
        if achievements >= Q3_ACHIEVEMENTS:
            raw_score += 1.0
        if platform_count >= 2:
            raw_score += 0.8
        if 2 <= genre_count <= 4:
            raw_score += 0.8
        if release_month in BEST_MONTHS:
            raw_score += 0.8

        # ── Massively Multiplayer note — F2P bias ──
        if 'Massively Multiplayer' in genres and not is_free:
            raw_score -= 0.5  # paid MMOs face extra barrier vs F2P norm

        score_out_of_10 = max(1.0, min(10.0, raw_score))

        # ── Tier mapping ──
        if score_out_of_10 >= 8.5:   tier = "Top-Tier Market Fit"
        elif score_out_of_10 >= 7.0: tier = "Highly Competitive"
        elif score_out_of_10 >= 5.5: tier = "Above Average"
        elif score_out_of_10 >= 4.0: tier = "Average Competitor"
        else:                        tier = "High Risk / Niche"

        cfg = TIER_CONFIG[tier]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎯 Hasil Evaluasi AI</div>', unsafe_allow_html=True)

        res_col, insight_col = st.columns([1, 1], gap="large")

        with res_col:
            st.markdown(f"""<div class="pred-result" style="border: 2px solid {cfg['color']}33; box-shadow: 0 0 40px {cfg['color']}15;">
<div style="font-size:3rem; margin-bottom:0.25rem;">{cfg['icon']}</div>
<div class="pred-result-label" style="color:#475569; font-size:0.8rem; margin-bottom:0.2rem;">KATEGORI PASAR</div>
<div class="pred-result-label" style="color:{cfg['color']}; font-size:1.5rem;">{tier.upper()}</div>
<div style="margin-top:1.5rem; padding-top:1rem; border-top:1px dashed {cfg['color']}55;">
<div style="color:#475569; font-size:0.75rem; font-family:'Orbitron', monospace; letter-spacing:1px;">COMPETITIVENESS RATING</div>
<div style="font-family:'JetBrains Mono',monospace; font-size:3.5rem; color:{cfg['color']}; font-weight:700; line-height:1.2;">
{score_out_of_10:.1f}<span style="font-size:1.5rem; color:#475569;">/10</span>
</div>
</div>
</div>""", unsafe_allow_html=True)

        with insight_col:
            st.markdown(f"""<div class="glass-card" style="border-color:{cfg['color']}33; height:100%;">
<div style="font-family:'Orbitron',monospace; font-size:0.75rem; letter-spacing:0.1em; color:{cfg['color']}; margin-bottom:1rem;">
DIAGNOSTIK FITUR
</div>
<div style="font-size:0.85rem; color:#475569; margin-bottom:1.5rem; line-height:1.6;">
{cfg['desc']}
</div>""", unsafe_allow_html=True)

            factors = [
                ("Pricing Strategy", "FREE" if is_free else f"${price:.2f}",
                 "🟢" if (is_free or price <= price_benchmark * 1.5) else "🔴"),
                ("Engagement Hooks", f"{achievements} Achv.",
                 "🟢" if achievements >= Q3_ACHIEVEMENTS else "🔴"),
                ("Platform Reach",   f"{platform_count} OS",
                 "🟢" if platform_count >= 2 else "🟡"),
                ("Niche Overlap",    f"{genre_count} Genres",
                 "🟢" if 2 <= genre_count <= 4 else "🔴"),
                ("Release Window",   f"Q{((release_month-1)//3)+1}",
                 "🟢" if release_month in BEST_MONTHS else "🟡"),
            ]

            for label, val, indicator in factors:
                if price > 50 and label == "Pricing Strategy": indicator = "🔴"
                if achievements == 0 and label == "Engagement Hooks": indicator = "🔴"

                st.markdown(f"""<div style="display:flex; justify-content:space-between; align-items:center; padding:6px 0; border-bottom:1px solid rgba(0,0,0,0.05);">
<span style="color:#334155; font-size:0.82rem; font-weight:500;">{label}</span>
<span style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; color:#0f172a;">{indicator} {val}</span>
</div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("💡 Rekomendasi Strategis Berdasarkan Data", expanded=True):
            recs = []

            recs.append("📢 **Golden Rule Steam:** Terlepas dari daya saing fitur, algoritma Steam sangat bergantung pada visibilitas awal. Pastikan Anda mengalokasikan waktu dan resource untuk *marketing* dan *wishlist building* secara agresif minimal 6 bulan sebelum rilis.")

            if not is_free and price > price_benchmark * 1.5:
                recs.append(f"💰 **Pricing:** Harga (${price:.2f}) melebihi 1.5x rata-rata median genre ini (${price_benchmark:.2f}). Dibutuhkan justification melalui visual atau gameplay depth yang kuat.")
            if achievements < Q3_ACHIEVEMENTS:
                recs.append(f"🏅 **Retention:** Tambahkan lebih banyak achievement (>{int(Q3_ACHIEVEMENTS)}). Data menunjukkan ini adalah cara efisien untuk menahan retention pemain.")
            if platform_count < 2:
                recs.append("🖥️ **Reach:** Kehilangan 10-15% audiens karena eksklusif di satu platform. Porting disarankan jika budget memungkinkan.")
            if genre_count < 2:
                recs.append("🎮 **Discoverability:** Terlalu sempit. Tambahkan 1 tag genre sekunder agar algoritma rekomendasi Steam lebih mudah mengkategorikan game Anda.")
            if genre_count > 4:
                recs.append("⚠️ **Identity Crisis:** Terlalu banyak genre bisa melemahkan target pasar utama. Fokus pada core gameplay loop.")
            if 'Massively Multiplayer' in genres and not is_free:
                recs.append("🌐 **MMO Pricing:** Mayoritas game Massively Multiplayer di Steam bersifat Free to Play. Game berbayar di kategori ini menghadapi barrier adopsi yang signifikan.")
            if selected_mature:
                recs.append(f"🔞 **Mature Content:** Genre {', '.join(selected_mature)} memerlukan proses verifikasi konten Steam yang lebih panjang. Alokasikan waktu tambahan untuk review pipeline sebelum launch.")

            for rec in recs:
                st.markdown(f"<div style='margin-bottom:0.5rem; font-size:0.9rem; color:#334155;'>{rec}</div>", unsafe_allow_html=True)