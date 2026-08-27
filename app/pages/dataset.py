# import streamlit as st
# import pandas as pd
# import numpy as np

# def show():
#     st.markdown("""
#     <div style="padding:2rem 0 1rem">
#         <div class="hero-subtitle">// DATA EXPLORATION</div>
#         <div class="hero-title" style="font-size:2rem;">Dataset Overview</div>
#         <p class="hero-desc" style="margin-top:0.6rem; font-size:0.9rem;">
#             Steam Games Dataset dari Kaggle (FronkonGames) — 71K+ game, 18 fitur utama.
#         </p>
#     </div>
#     """, unsafe_allow_html=True)

#     # Dataset info cards
#     st.markdown('<div class="section-title">📦 Informasi Dataset</div>', unsafe_allow_html=True)

#     cols = st.columns(4)
#     stats = [
#         ("71,532", "Total Records",   "🎮"),
#         ("18",     "Fitur / Kolom",   "📋"),
#         ("2003–2024","Rentang Tahun", "📅"),
#         ("Kaggle",  "Sumber Data",    "🌐"),
#     ]
#     for i, (val, label, icon) in enumerate(stats):
#         with cols[i]:
#             st.metric(f"{icon} {label}", val)

#     st.markdown("<br>", unsafe_allow_html=True)

#     # Feature table
#     st.markdown('<div class="section-title">🗂️ Fitur Dataset</div>', unsafe_allow_html=True)

#     features = pd.DataFrame({
#         "Fitur": ["appID","name","release_date","price","positive","negative",
#                   "peak_ccu","recommendations","achievements","genres",
#                   "categories","tags","windows","mac","linux",
#                   "average_playtime_forever","median_playtime_forever","estimated_owners"],
#         "Tipe":  ["int","str","str","float","int","int","int","int","int",
#                   "str","str","str","bool","bool","bool","float","float","str"],
#         "Deskripsi": [
#             "ID unik aplikasi Steam", "Nama game",
#             "Tanggal rilis", "Harga dalam USD",
#             "Jumlah ulasan positif", "Jumlah ulasan negatif",
#             "Puncak pengguna bersamaan", "Jumlah rekomendasi",
#             "Jumlah achievement", "Genre game",
#             "Kategori fitur game", "Tag komunitas Steam",
#             "Dukungan Windows", "Dukungan macOS", "Dukungan Linux",
#             "Rata-rata playtime seumur hidup", "Median playtime seumur hidup",
#             "Estimasi jumlah pemilik (range)",
#         ],
#         "Digunakan": ["—","—","✅","✅","✅","✅","✅","✅","✅","✅","—","—","✅","✅","✅","✅","✅","✅"],
#     })
#     st.dataframe(features, use_container_width=True, hide_index=True)

#     st.markdown("<br>", unsafe_allow_html=True)

#     # Engineered features
#     st.markdown('<div class="section-title">⚗️ Feature Engineering</div>', unsafe_allow_html=True)

#     eng = [
#         ("positive_ratio",      "Rasio ulasan positif", "positive / (total_reviews + 1)"),
#         ("engagement_score",    "Skor keterlibatan pemain", "average_playtime × log(peak_ccu + 1)"),
#         ("market_impact_score", "Skor dampak pasar (target labeling)",
#          "0.30×owners + 0.25×ccu + 0.20×engagement + 0.15×recommendations + 0.10×positive_ratio"),
#         ("success_label",       "Label tier keberhasilan",
#          "Failure / Moderate / Successful / Hit / Generational Hit"),
#         ("platform_count",      "Jumlah platform yang didukung", "windows + mac + linux"),
#         ("genre_X",             "One-hot encoding genre",        "1 jika memiliki genre X, else 0"),
#     ]

#     for name, desc, formula in eng:
#         with st.expander(f"**`{name}`** — {desc}"):
#             st.code(formula, language="python")

#     # Distribution info
#     st.markdown("<br>", unsafe_allow_html=True)
#     st.markdown('<div class="section-title">📊 Distribusi Target Label</div>', unsafe_allow_html=True)

#     dist = pd.DataFrame({
#         "Tier": ["Failure", "Moderate", "Successful", "Hit", "Generational Hit"],
#         "Jumlah (approx)": [32400, 18900, 12600, 5700, 1932],
#         "Persentase": ["45.3%", "26.4%", "17.6%", "8.0%", "2.7%"],
#     })
#     st.dataframe(dist, use_container_width=True, hide_index=True)

#     st.info("⚖️ **Class Imbalance**: Karena distribusi tidak merata, SMOTE digunakan saat training untuk menyeimbangkan kelas Successful, Hit, dan Generational Hit.")

#     st.markdown("<br>", unsafe_allow_html=True)
#     st.markdown('<div class="section-title">🔗 Sumber Dataset</div>', unsafe_allow_html=True)
#     st.markdown("""
#     <div class="glass-card">
#         <div style="font-family:'JetBrains Mono',monospace; font-size:0.82rem; color:#475569; margin-bottom:0.5rem;">SOURCE</div>
#         <div style="font-size:0.9rem; color:#0f172a; margin-bottom:0.3rem;">
#             <strong>FronkonGames/steam-games-dataset</strong>
#         </div>
#         <div style="font-size:0.82rem; color:#475569;">
#             Platform: Hugging Face Datasets / Kaggle<br>
#             Lisensi: CC BY 4.0<br>
#             URL: <code style="color:#0369a1;">huggingface.co/datasets/FronkonGames/steam-games-dataset</code>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)


import streamlit as st
import pandas as pd
import numpy as np
import os

# 1. CACHED DATA LOADER
@st.cache_data
def load_data():
    # Navigates from app/pages/dataset.py -> app/pages -> app -> root -> data -> csv
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'steam_games_clustered.csv'))
    return pd.read_csv(csv_path)

def show():
    st.markdown("""
    <div style="padding:2rem 0 1rem">
        <div class="hero-subtitle">// DATA EXPLORATION</div>
        <div class="hero-title" style="font-size:2rem;">Dataset Overview</div>
        <p class="hero-desc" style="margin-top:0.6rem; font-size:0.9rem;">
            Steam Games Dataset dari Kaggle (FronkonGames) setelah melalui proses Pre-Processing dan Clustering.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. LOAD DATA
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("⚠️ File steam_games_clustered.csv tidak ditemukan di folder data/. Pastikan file sudah dipindahkan.")
        return

    # 3. DYNAMIC DATASET INFO CARDS
    st.markdown('<div class="section-title">📦 Informasi Dataset</div>', unsafe_allow_html=True)
    
    # Calculate years safely depending on what the column is named in your CSV
    # Calculate years safely depending on what the column is named in your CSV
    df['year'] = df['release_date'].astype(str).str.extract(r'(19\d{2}|20\d{2})').astype(float)
    
    # Calculate range safely
    valid_years = df['year'].dropna()
    if not valid_years.empty:
        min_year = int(valid_years.min())
        max_year = int(valid_years.max())
        year_range = f"{min_year} – {max_year}"
    else:
        year_range = "Data Unavailable"

        
    cols = st.columns(4)
    stats = [
        (f"{len(df):,}", "Total Records",   "🎮"),
        (f"{len(df.columns)}", "Fitur / Kolom", "📋"),
        (year_range, "Rentang Tahun", "📅"),
        ("Kaggle",  "Sumber Data",    "🌐"),
    ]
    for i, (val, label, icon) in enumerate(stats):
        with cols[i]:
            st.metric(f"{icon} {label}", val)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. RAW DATA PREVIEW
    st.markdown('<div class="section-title">🗂️ Preview Data Nyata</div>', unsafe_allow_html=True)
    st.dataframe(df.head(100), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Engineered features logic (Kept intact for documentation)
    st.markdown('<div class="section-title">⚗️ Feature Engineering</div>', unsafe_allow_html=True)

    eng = [
        ("positive_ratio",      "Rasio ulasan positif", "positive / (total_reviews + 1)"),
        ("engagement_score",    "Skor keterlibatan pemain", "average_playtime × log(peak_ccu + 1)"),
        ("market_impact_score", "Skor dampak pasar (target labeling)",
         "0.30×owners + 0.25×ccu + 0.20×engagement + 0.15×recommendations + 0.10×positive_ratio"),
        ("success_label",       "Label tier keberhasilan",
         "Failure / Moderate / Successful / Hit / Generational Hit"),
        ("platform_count",      "Jumlah platform yang didukung", "windows + mac + linux"),
        ("genre_X",             "One-hot encoding genre",        "1 jika memiliki genre X, else 0"),
    ]

    for name, desc, formula in eng:
        with st.expander(f"**`{name}`** — {desc}"):
            st.code(formula, language="python")

    # 5. DYNAMIC TARGET DISTRIBUTION
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Distribusi Target Label (Nyata)</div>', unsafe_allow_html=True)

    # Check for 'success_label' or 'Tier' depending on what it was saved as
    target_col = 'success_label' if 'success_label' in df.columns else 'Tier' if 'Tier' in df.columns else None

    if target_col:
        # Calculate actual distribution
        tier_counts = df[target_col].value_counts().reset_index()
        tier_counts.columns = ['Tier', 'Jumlah']
        tier_counts['Persentase'] = (tier_counts['Jumlah'] / len(df) * 100).round(1).astype(str) + '%'
        
        # Sort them in logical order rather than just count
        tier_order = {"Failure": 1, "Moderate": 2, "Successful": 3, "Hit": 4, "Generational Hit": 5}
        tier_counts['sort_order'] = tier_counts['Tier'].map(tier_order)
        tier_counts = tier_counts.sort_values('sort_order').drop('sort_order', axis=1)
        
        st.dataframe(tier_counts, use_container_width=True, hide_index=True)
    else:
        # If it still fails, this will print out exactly what columns DO exist so you can debug it
        st.warning(f"⚠️ Kolom target tidak ditemukan. Kolom yang ada di CSV Anda: {', '.join(df.columns.tolist()[:10])}...")

    st.info("⚖️ **Class Imbalance**: Karena distribusi tidak merata, SMOTE digunakan saat training untuk menyeimbangkan kelas Successful, Hit, dan Generational Hit.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🔗 Sumber Dataset</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.82rem; color:#475569; margin-bottom:0.5rem;">SOURCE</div>
        <div style="font-size:0.9rem; color:#0f172a; margin-bottom:0.3rem;">
            <strong>FronkonGames/steam-games-dataset</strong>
        </div>
        <div style="font-size:0.82rem; color:#475569;">
            Platform: Hugging Face Datasets / Kaggle<br>
            Lisensi: CC BY 4.0<br>
            URL: <code style="color:#0369a1;">huggingface.co/datasets/FronkonGames/steam-games-dataset</code>
        </div>
    </div>
    """, unsafe_allow_html=True)