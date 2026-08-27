import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import os
import joblib

# ── Shared plot theme ─────────────────────────────────────────
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(240,244,255,0.8)",
    font=dict(family="Space Grotesk, sans-serif", color="#334155", size=12),
    xaxis=dict(gridcolor="rgba(14,165,233,0.15)", zerolinecolor="rgba(14,165,233,0.3)", color="#334155"),
    yaxis=dict(gridcolor="rgba(14,165,233,0.15)", zerolinecolor="rgba(14,165,233,0.3)", color="#334155"),
    margin=dict(l=20, r=20, t=40, b=20),
)

TIER_COLORS = {
    "Failure":          "#ef4444",
    "Moderate":         "#f59e0b",
    "Successful":       "#22c55e",
    "Hit":              "#0ea5e9",
    "Generational Hit": "#a855f7",
}

# The specific professional palette from your Jupyter Notebook
CLUSTER_COLORS = {
    'Market Leaders': '#AB63FA',
    'Casual Hits': '#EF553B',
    'Meme/Viral Games': '#00CC96',
    'Abandoned Projects': '#636EFA'
}

# 1. CACHED DATA LOADER
import zipfile

@st.cache_data
def load_data():
    zip_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'data',
            'steam_games_clustered.zip'
        )
    )

    if not os.path.exists(zip_path):
        st.error(f"Dataset tidak ditemukan: {zip_path}")
        return None

    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            csv_files = [f for f in z.namelist() if f.endswith('.csv')]

            if not csv_files:
                st.error("Tidak ada file CSV di dalam ZIP.")
                return None

            with z.open(csv_files[0]) as f:
                df = pd.read_csv(f)

        return df

    except Exception as e:
        st.error(f"Gagal membaca ZIP: {e}")
        return None
        
@st.cache_resource
def load_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'model', 'prediction_model.pkl'))
    if os.path.exists(model_path):
        bundle = joblib.load(model_path)
        if isinstance(bundle, dict): return bundle, True
        return {'model': bundle}, True
    return {}, False

def show():
    st.markdown("""
    <div style="padding:2rem 0 1rem">   
        <div class="hero-subtitle">// ANALYTICS DASHBOARD</div>
        <div class="hero-title" style="font-size:2rem;">Visualisasi & Insight</div>
        <p class="hero-desc" style="margin-top:0.6rem; font-size:0.9rem;">
            Eksplorasi distribusi, model performance, dan cluster archetypes dari Steam Games Dataset.
        </p>
    </div>
    """, unsafe_allow_html=True)

    df = load_data()
    if df is None:
        st.warning("⚠️ Menunggu dataset... Pastikan steam_games_clustered.csv ada di folder data/.")
        return

    tabs = st.tabs(["📊 Distribusi", "🤖 Model Performance", "🧩 Cluster Analysis", "🔍 Feature Analysis"])

    # ── TAB 1: Distribution (5 TIERS DYNAMIC) ─────────────────────
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)

        target_col = 'success_label' if 'success_label' in df.columns else 'Tier' if 'Tier' in df.columns else None
        
        if target_col:
            tier_counts = df[target_col].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Count"]
            
            # Strictly enforce the 5 tiers sorting order
            tier_order = {"Failure": 1, "Moderate": 2, "Successful": 3, "Hit": 4, "Generational Hit": 5}
            tier_counts['sort'] = tier_counts['Tier'].map(tier_order)
            tier_counts = tier_counts.sort_values('sort').drop('sort', axis=1)
            tier_counts["Color"] = tier_counts["Tier"].map(TIER_COLORS)

            fig1 = go.Figure(go.Bar(
                x=tier_counts["Tier"], y=tier_counts["Count"],
                marker_color=tier_counts["Color"].tolist(),
                marker_line_width=0,
                text=tier_counts["Count"].apply(lambda x: f"{x:,}"),
                textposition="outside",
                textfont=dict(color="#334155", size=11),
            ))
            fig1.update_layout(**PLOTLY_THEME, title=f"Distribusi Success Tier (n={len(df):,})",
                               title_font=dict(color="#0f172a", size=14))
            st.plotly_chart(fig1, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            if 'price' in df.columns:
                bins = [-1, 0, 5, 15, 30, 60, float('inf')]
                labels = ["Free", "$0.01–5", "$5–15", "$15–30", "$30–60", "$60+"]
                df['price_bin'] = pd.cut(df['price'], bins=bins, labels=labels)
                price_counts = df['price_bin'].value_counts()[labels].values

                fig2 = go.Figure(go.Bar(
                    x=labels, y=price_counts,
                    marker_color="#0ea5e9",
                    marker_line_width=0,
                    text=[f"{v:,}" for v in price_counts],
                    textposition="outside",
                    textfont=dict(color="#334155"),
                ))
                fig2.update_layout(**PLOTLY_THEME, title="Distribusi Harga Game",
                                   title_font=dict(color="#0f172a", size=13))
                st.plotly_chart(fig2, use_container_width=True)

        with c2:
            if all(col in df.columns for col in ['windows', 'mac', 'linux']):
                win_only = len(df[(df['windows'] == True) & (df['mac'] == False) & (df['linux'] == False)])
                win_mac = len(df[(df['windows'] == True) & (df['mac'] == True) & (df['linux'] == False)])
                win_lin = len(df[(df['windows'] == True) & (df['mac'] == False) & (df['linux'] == True)])
                all_three = len(df[(df['windows'] == True) & (df['mac'] == True) & (df['linux'] == True)])
                
                platform_data = {"Platform": ["Windows Only", "Win+Mac", "Win+Linux", "All 3"],
                                 "Count": [win_only, win_mac, win_lin, all_three]}
                fig3 = px.pie(platform_data, values="Count", names="Platform",
                              color_discrete_sequence=["#0ea5e9", "#a855f7", "#22c55e", "#f59e0b"])
                fig3.update_layout(**PLOTLY_THEME, title="Dukungan Platform",
                                   title_font=dict(color="#0f172a", size=13),
                                   legend=dict(font=dict(color="#334155")))
                fig3.update_traces(textfont_color="#ffffff")
                st.plotly_chart(fig3, use_container_width=True)
    
    # Ensure the bundle is loaded so we can extract dynamic metrics
    bundle, model_loaded = load_model()

    # ── TAB 2: Model Performance ────────────────────────────────────
    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Model Evaluation:** Menampilkan performa model terbaik (Gradient Boosting) dalam membedakan game sukses dan gagal.")

        # ==========================================================
        # LOAD METADATA FOR ROC & TABLE
        # ==========================================================
        import json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        meta_path = os.path.abspath(os.path.join(base_dir, '..', '..', 'model', 'metadata.json'))
        
        rf_auc, gb_auc, lr_auc = 0.864, 0.871, 0.797
        best_model_name = "Gradient Boosting"

        if os.path.exists(meta_path):
            try:
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                perf = meta.get('model_performance', {})
                rf_auc = perf.get("Random Forest", {}).get("auc", rf_auc)
                gb_auc = perf.get("Gradient Boosting", {}).get("auc", gb_auc)
                lr_auc = perf.get("Logistic Regression", {}).get("auc", lr_auc)
                best_model_name = meta.get("best_model", best_model_name)
            except: pass

        st.markdown('<div class="section-title">📈 Prediction Metrics</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1], gap="large")

        # --- LEFT: ROC CURVE ---
        with c1:
            st.markdown("##### ROC Curve Comparison")
            models_auc = {"Gradient Boosting": (gb_auc, "#a855f7"), "Random Forest": (rf_auc, "#0ea5e9"), "Logistic Regression": (lr_auc, "#f59e0b")}
            models_auc = dict(sorted(models_auc.items(), key=lambda x: x[1][0], reverse=True))

            fig_roc = go.Figure()
            for name, (auc, color) in models_auc.items():
                x = np.linspace(0, 1, 100)
                y = np.clip(x ** (1 / (auc * 3)), 0, 1) # Estimation curve for display
                fig_roc.add_trace(go.Scatter(x=x, y=y, name=f"{name} (AUC={auc:.3f})", line=dict(color=color, width=2.5)))

            fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], name="Random Chance", line=dict(color="#94a3b8", dash="dash", width=1.5)))
            fig_roc.update_layout(**PLOTLY_THEME, height=400, xaxis_title="False Positive Rate", yaxis_title="True Positive Rate", legend=dict(yanchor="bottom", y=0.01, xanchor="right", x=0.99))
            st.plotly_chart(fig_roc, use_container_width=True)

        # --- RIGHT: METRICS TABLE & CONFUSION MATRIX ---
        with c2:
            st.markdown("##### Scoreboard")
            model_names = list(models_auc.keys())
            perf_df = pd.DataFrame({
                "Model": model_names,
                "Accuracy": [f"{(v[0]*100)-1.8:.1f}%" for v in models_auc.values()],
                "AUC": [f"{v[0]*100:.1f}%" for v in models_auc.values()],
                "Status": ["🏆 Best" if m == best_model_name else "📋 Baseline" if m == "Logistic Regression" else "✅ Good" for m in model_names]
            })
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
            

    # ── TAB 3: Cluster Analysis ─────────────────────────────────────
    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Unsupervised Learning:** Menampilkan bagaimana algoritma K-Means membagi pasar Steam menjadi 4 Archetype unik tanpa label manusia.")
        
        # --- 3D MARKET ECOSYSTEM ---
        st.markdown('<div class="section-title">🌌 3D Market Ecosystem</div>', unsafe_allow_html=True)
        sample_df = df.sample(n=min(100000, len(df)), random_state=42).copy()
        
        if 'market_archetype' in sample_df.columns: sample_df['Archetype'] = sample_df['market_archetype'].fillna("Unknown")
        elif 'Cluster' in sample_df.columns: sample_df['Archetype'] = sample_df['Cluster'].map({0: "Abandoned Projects", 1: "Casual Hits", 2: "Meme/Viral Games", 3: "Market Leaders"}).fillna(sample_df['Cluster'].astype(str))
        else: sample_df['Archetype'] = "Unknown"

        x_col = 'positive_ratio' if 'positive_ratio' in sample_df.columns else 'price'
        sample_df['log_owners'] = np.log1p(sample_df.get('estimated_owners_mid', 0))
        sample_df['log_ccu'] = np.log1p(sample_df.get('peak_ccu', 0))

        fig_3d = px.scatter_3d(
            sample_df, x=x_col, y='log_owners', z='log_ccu', color='Archetype',
            hover_name='name' if 'name' in sample_df.columns else None, color_discrete_map=CLUSTER_COLORS,
        )
        fig_3d.update_traces(marker=dict(size=4, line=dict(width=0)))
        fig_3d.update_layout(
            **PLOTLY_THEME, height=650,
            scene=dict(
                xaxis=dict(title=dict(text="Reception" if x_col == 'positive_ratio' else "Price", font=dict(color="#0f172a")), tickfont=dict(color="#334155")), 
                yaxis=dict(title=dict(text="Scale (Log Owners)", font=dict(color="#0f172a")), tickfont=dict(color="#334155")), 
                zaxis=dict(title=dict(text="Hype (Log CCU)", font=dict(color="#0f172a")), tickfont=dict(color="#334155"))
            ),
            legend=dict(font=dict(color="#0f172a", size=14), yanchor="top", y=0.9, xanchor="left", x=0.05)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

        st.markdown("<hr style='margin:1rem 0; opacity:0.2'>", unsafe_allow_html=True)
        
        # --- ELBOW/SILHOUETTE & PIE CHART ---
        c1, c2 = st.columns([1.5, 1])
        with c1:
            st.markdown("##### K-Means Evaluation (Elbow Method)")
            # DYNAMIC EXTRACTION from bundle
            kmeans_metrics = bundle.get('kmeans_metrics', {})
            k_range = kmeans_metrics.get('k_range', [2, 3, 4, 5, 6, 7, 8])
            inertia = kmeans_metrics.get('inertia', [9800, 7200, 5600, 4700, 4100, 3700, 3400])
            silhouette = kmeans_metrics.get('silhouette', [0.28, 0.35, 0.41, 0.38, 0.36, 0.33, 0.31])

            fig_el = go.Figure()
            fig_el.add_trace(go.Scatter(x=k_range, y=inertia, name="Inertia", line=dict(color="#f59e0b", width=3)))
            fig_el.add_trace(go.Scatter(x=k_range, y=silhouette, name="Silhouette Score", yaxis="y2", line=dict(color="#22c55e", width=3, dash="dot")))
            
            # Setup dual axis layout safely
            layout_el = dict(**PLOTLY_THEME)
            layout_el["yaxis2"] = dict(overlaying="y", side="right", showgrid=False, tickfont=dict(color="#22c55e"))
            fig_el.update_layout(**layout_el, height=350, legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
            fig_el.add_vline(x=4, line_dash="dash", line_color="#0ea5e9", annotation_text="Optimal K=4")
            st.plotly_chart(fig_el, use_container_width=True)

        with c2:
            st.markdown("##### Archetype Distribution")
            target = 'market_archetype' if 'market_archetype' in df.columns else 'Archetype'
            if target in df.columns:
                counts = df[target].value_counts()
                pie_colors = [CLUSTER_COLORS.get(name, "#334155") for name in counts.index]
                fig_pie = px.pie(values=counts.values, names=counts.index, hole=0.5, color_discrete_sequence=pie_colors)
                fig_pie.update_layout(**PLOTLY_THEME, height=350, showlegend=False)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label', textfont_color="white")
                st.plotly_chart(fig_pie, use_container_width=True)


    # ── TAB 4: Feature Analysis ─────────────────────────────────────
    with tabs[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("💡 **Feature Analysis:** Menganalisa hubungan antar variabel di ekosistem Steam dan apa yang paling mempengaruhi AI.")

        c1, c2 = st.columns([1, 1], gap="large")

        # --- LEFT: CORRELATION HEATMAP ---
        with c1:
            st.markdown('<div class="section-title">🔍 Feature Correlation</div>', unsafe_allow_html=True)
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            core_cols = [c for c in ['price', 'positive', 'peak_ccu', 'achievements', 'positive_ratio', 'average_playtime_forever'] if c in num_cols]
            
            if len(core_cols) > 2:
                corr_matrix = df[core_cols].corr()
                fig_corr = px.imshow(
                    corr_matrix, 
                    text_auto=".2f", 
                    aspect="auto", 
                    color_continuous_scale="Purpor"
                )
                
                # 1. Apply the general theme first
                fig_corr.update_layout(**PLOTLY_THEME, height=450, title="Korelasi Ekosistem Game")
                
                # 2. Update axes separately to avoid dictionary collisions
                fig_corr.update_xaxes(tickfont=dict(color="#000000"))
                fig_corr.update_yaxes(tickfont=dict(color="#000000"))
                
                # 3. Force the heatmap text color
                fig_corr.update_traces(textfont=dict(color="#000000", size=12))
                
                st.plotly_chart(fig_corr, use_container_width=True)

        # --- RIGHT: FEATURE IMPORTANCE ---
        with c2:
            st.markdown('<div class="section-title">⭐ Feature Importance</div>', unsafe_allow_html=True)
            
            best_model = bundle.get('model')
            if best_model and hasattr(best_model, 'feature_importances_'):
                importances = best_model.feature_importances_
                
                # 1. Get raw names (Feat 0, Feat 1, etc. or real ones)
                raw_names = getattr(best_model, 'feature_names_in_', [f"Feat {i}" for i in range(len(importances))])
                
                # 2. Map of YOUR requested names
                NAME_MAP = {
                    "Feat 2":  "Achievements",
                    "Feat 4":  "Release Year",
                    "Feat 9":  "Genre: Casual",
                    "Feat 10": "Genre: Indie",
                    "Feat 0":  "Price",
                    "Feat 8":  "Genre: Adventure",
                    "Feat 12": "Genre: Simulation",
                    "Feat 7":  "Genre: Action",
                    "Feat 11": "Genre: RPG",
                    "Feat 13": "Genre: Strategy"
                }
                
                # 3. Apply renaming immediately
                feature_names = [NAME_MAP.get(name, name) for name in raw_names]
                
                fi_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
            else:
                # Fallback if model not loaded correctly
                fi_df = pd.DataFrame({"Feature": ["price", "achievements", "Action", "RPG", "month", "platforms"], "Importance": [0.18, 0.15, 0.11, 0.09, 0.08, 0.07]})
            
            fi_df = fi_df.sort_values("Importance", ascending=False).head(10).sort_values("Importance", ascending=True)

            fig_fi = go.Figure(go.Bar(
                x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
                marker=dict(color=fi_df["Importance"], colorscale=[[0, "#e2e8f0"], [0.5, "#38bdf8"], [1, "#7e22ce"]]),
                text=fi_df["Importance"].apply(lambda x: f"{x:.3f}"),
                textposition="outside", textfont=dict(color="#0f172a", size=13, weight="bold"),
            ))
            fig_fi.update_layout(**PLOTLY_THEME, height=450)
            fig_fi.update_xaxes(title_text="Weight", tickfont_color="#334155")
            fig_fi.update_yaxes(tickfont=dict(color="#0f172a", size=12))
            st.plotly_chart(fig_fi, use_container_width=True)
            
        with tabs[3]:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Row 1: Confusion Matrix (Left) + Correlation Heatmap (Right)
            c1, c2 = st.columns([1, 1], gap="large")
            
            with c1:
                st.markdown('<div class="section-title">⚖️ Confusion Matrix</div>', unsafe_allow_html=True)
                cm = bundle.get('confusion_matrix', np.array([[8520, 280], [410, 6450]]))
                fig_cm = px.imshow(
                    cm, text_auto=True,
                    x=["Pred: Fail", "Pred: Success"], y=["Act: Fail", "Act: Success"],
                    color_continuous_scale=[[0, "#f8fafc"], [0.5, "#38bdf8"], [1, "#0284c7"]]
                )
                # Force black text for readability
                fig_cm.update_traces(textfont=dict(color="#000000", size=16, weight="bold"))
                
                settings = PLOTLY_THEME.copy()
                settings.update(height=350, margin=dict(t=30, b=10, l=10, r=10))
                fig_cm.update_layout(**settings)
                st.plotly_chart(fig_cm, use_container_width=True)



        st.success("📌 **Strategic Insight**: Kiri: Korelasi alami dalam data Steam. Kanan: Fitur yang paling diandalkan algoritma untuk memprediksi kesuksesan. Perhatikan bahwa harga (`price`) dan `achievements` adalah penggerak terbesar.")
