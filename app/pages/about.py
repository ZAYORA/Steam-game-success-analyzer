import streamlit as st
import pandas as pd
import json
import os

def load_meta():
    """Loads metadata from the model folder."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    meta_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'model', 'metadata.json'))
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def get_dataset_size():
    """Counts games from the dataset."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'dataset', 'steam_games_clustered.csv'))
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            return f"{len(df):,}"
        except:
            return "124,146"
    return "124,146"

def show():
    meta = load_meta()
    total_games = get_dataset_size()
    
    # Dynamic Variables
    best_model = meta.get('best_model', 'Gradient Boosting')
    k_clusters = meta.get('k_clusters', 4)
    sil_score = meta.get('silhouette_score', 0.658)
    
    # Safely get AUC for the best model
    perf = meta.get('model_performance', {})
    auc_score = perf.get(best_model, {}).get('auc', 0.871)

    st.markdown("""
    <div style="padding:2rem 0 1rem">
        <div class="hero-subtitle">// PROJECT DOCUMENTATION</div>
        <div class="hero-title" style="font-size:2rem;">About This Project</div>
    </div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["🔬 Metodologi", "📦 Dataset", "⚙️ Sistem", "📎 Lampiran"])

    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">🔬 Metode Data Mining</div>', unsafe_allow_html=True)

        with st.expander(f"🤖 **{best_model} Classification**", expanded=True):
            st.markdown(f"""
            {best_model} dipilih sebagai model klasifikasi utama untuk memprediksi sukses peluncuran game.

            **Performa:**
            - AUC-ROC: **{auc_score*100:.2f}%**
            - Imbalanced handling: SMOTE oversampling pada training set

            **Mengapa dipilih?** {best_model} terbukti memberikan hasil paling akurat dalam menangani fitur campuran dataset Steam.
            """)

        with st.expander(f"🧩 **K-Means Clustering (k={k_clusters})**", expanded=True):
            arch_list = [v for v in meta.get('archetype_map', {}).values()]
            arch_str = " · ".join(arch_list) if arch_list else "Market Leaders · Casual Hits · Meme/Viral Games · Abandoned Projects"
            
            st.markdown(f"""
            K-Means mengelompokkan game berdasarkan kemiripan profil pasar menjadi {k_clusters} segmen.

            **Hasil Evaluasi:**
            - Silhouette Score: **{sil_score:.4f}**
            - Optimal k: {k_clusters} (ditetapkan melalui Elbow Method)

            **Market Archetypes:**
            {arch_str}
            """)

        st.markdown('<div class="section-title" style="margin-top:1.5rem;">📐 Framework CRISP-DM</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            Proyek ini mengikuti framework <strong style="color:#00d4ff">CRISP-DM</strong>
            (Cross Industry Standard Process for Data Mining):
            <ol style="margin-top:0.8rem; line-height:2.2; color:#475569; font-size:0.88rem;">
                <li><strong style="color:#e2e8f0">Business Understanding</strong> — Identifikasi faktor sukses game Steam</li>
                <li><strong style="color:#e2e8f0">Data Understanding</strong> — Eksplorasi 124K+ game</li>
                <li><strong style="color:#e2e8f0">Data Preparation</strong> — Cleaning, feature engineering, SMOTE</li>
                <li><strong style="color:#e2e8f0">Modeling</strong> — Random Forest + K-Means</li>
                <li><strong style="color:#e2e8f0">Evaluation</strong> — AUC, Silhouette, Confusion Matrix</li>
                <li><strong style="color:#e2e8f0">Deployment</strong> — Aplikasi Streamlit web</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="glass-card">
            <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:#0369a1;
                        letter-spacing:0.1em; margin-bottom:1rem;">DATASET DETAILS</div>
            <table style="width:100%; border-collapse:collapse; font-size:0.88rem;">
                <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
                    <td style="color:#475569; padding:8px 0; width:40%;">Nama Dataset</td>
                    <td style="color:#0f172a;">Steam Games Dataset</td></tr>
                <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
                    <td style="color:#475569; padding:8px 0;">Sumber</td>
                    <td style="color:#0369a1;">FronkonGames (Hugging Face / Kaggle)</td></tr>
                <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
                    <td style="color:#475569; padding:8px 0;">Jumlah Record</td>
                    <td style="color:#0f172a;">{total_games} games</td></tr>
                <tr style="border-bottom:1px solid rgba(0,212,255,0.1);">
                    <td style="color:#475569; padding:8px 0;">Lisensi</td>
                    <td style="color:#0f172a;">CC BY 4.0</td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">⚙️ Tech Stack</div>', unsafe_allow_html=True)

        tech_items = [
            ("🐍 Python 3.11",       "Bahasa pemrograman utama"),
            ("📊 Pandas / NumPy",    "Manipulasi dan analisis data"),
            ("🤖 Scikit-learn",      "Model ML: Random Forest, K-Means, SMOTE"),
            ("📈 Plotly / Seaborn",  "Visualisasi data interaktif"),
            ("🌐 Streamlit",         "Framework web app deployment"),
            ("💾 Joblib",            "Serialisasi model ke .pkl"),
            ("📓 Jupyter Notebook",  "Eksplorasi & development notebook"),
        ]

        cols = st.columns(2)
        for i, (tech, desc) in enumerate(tech_items):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="glass-card" style="padding:1rem; margin-bottom:0.6rem; display:flex; gap:1rem; align-items:center;">
                    <div style="font-size:1.2rem;">{tech.split()[0]}</div>
                    <div>
                        <div style="font-family:'Space Grotesk',sans-serif; font-weight:600;
                                    font-size:0.88rem; color:#0f172a;">{" ".join(tech.split()[1:])}</div>
                        <div style="font-size:0.78rem; color:#475569;">{desc}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    with tabs[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-title">📎 Lampiran & Tautan</div>', unsafe_allow_html=True)

        links = [
            ("📦 Dataset",                 "🔗 Lihat Dataset",    "https://huggingface.co/datasets/FronkonGames/steam-games-dataset", "#00d4ff"),
            ("💻 Source Code Notebook",    "🔗 Buka Notebook",    "https://github.com/username/steam-analyzer/blob/main/notebook/analysisV2.ipynb", "#bf5fff"),
            ("🌐 Aplikasi (Live Demo)",    "🔗 Buka Aplikasi",    "https://steam-analyzer.streamlit.app", "#39ff14"),
            ("🎬 Video Presentasi",        "🔗 Tonton Video",     "https://youtube.com/watch?v=XXXXX", "#ffd700"),
            ("📁 Repository Project",      "🔗 GitHub Repo",      "https://github.com/username/steam-analyzer", "#00d4ff"),
            ("📄 Laporan Artikel (PDF)",   "🔗 Unduh Laporan",    "https://drive.google.com/file/XXXXX", "#ff4757"),
        ]

        for title, btn_label, url, color in links:
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:0.75rem; display:flex;
                         justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-weight:600; font-size:0.9rem; color:#0f172a;">{title}</div>
                    <div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem;
                                color:#475569; margin-top:2px;">{url[:60]}...</div>
                </div>
                <a href="{url}" target="_blank" style="
                    display:inline-block; padding:6px 14px;
                    background:transparent; border:1px solid {color};
                    color:{color}; border-radius:6px; font-size:0.75rem;
                    font-family:'Orbitron',monospace; text-decoration:none;
                    letter-spacing:0.05em; white-space:nowrap;
                    transition:all 0.2s;">{btn_label}</a>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info("⚠️ Ganti placeholder URL di atas dengan link asli setelah upload ke repository/hosting.")
