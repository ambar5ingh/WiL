import streamlit as st
import pandas as pd
import numpy as np
import io
import os
from scipy import stats

st.set_page_config(
    page_title="WiL · Research Data Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --navy:   #0d1f3c;
    --teal:   #1a7a6e;
    --gold:   #c9a84c;
    --cream:  #f5f0e8;
    --white:  #ffffff;
    --mid:    #6b7a8d;
    --green:  #2e7d52;
    --red:    #b84444;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--navy);
}

.hero {
    background: linear-gradient(135deg, var(--navy) 0%, #1c3557 60%, var(--teal) 100%);
    padding: 2.4rem 2.8rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 220px; height: 220px;
    border-radius: 50%;
    background: rgba(201,168,76,.15);
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--white);
    margin: 0 0 .3rem;
}
.badge {
    display: inline-block;
    background: var(--gold);
    color: var(--navy);
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: .06em;
    text-transform: uppercase;
    padding: .22rem .7rem;
    border-radius: 20px;
    margin-right: .4rem;
    margin-top: .5rem;
}

[data-testid="stSidebar"] { background-color: var(--navy) !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,.88) !important; }

.card {
    background: var(--white);
    border-radius: 10px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(13,31,60,.08);
    box-shadow: 0 2px 12px rgba(13,31,60,.06);
}
.card h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: var(--navy);
    margin-bottom: .6rem;
    border-left: 3px solid var(--gold);
    padding-left: .7rem;
}

.metric-row { display: flex; gap: 1rem; flex-wrap: wrap; margin-bottom: 1rem; }
.metric-tile {
    flex: 1;
    min-width: 130px;
    background: linear-gradient(135deg, var(--navy), #1c3557);
    color: var(--white);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-tile .val {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: var(--gold);
    line-height: 1;
}
.metric-tile .lbl { font-size: .75rem; opacity: .75; margin-top: .3rem; letter-spacing:.04em; text-transform:uppercase; }

.stat-tile {
    background: var(--white);
    border: 1px solid rgba(13,31,60,.10);
    border-radius: 10px;
    padding: .9rem 1.1rem;
    text-align: center;
    box-shadow: 0 1px 6px rgba(13,31,60,.05);
}
.stat-tile .sval {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--teal);
    line-height: 1.1;
}
.stat-tile .slbl {
    font-size: .72rem;
    color: var(--mid);
    margin-top: .2rem;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.sig-badge {
    display: inline-block;
    padding: .18rem .65rem;
    border-radius: 20px;
    font-size: .75rem;
    font-weight: 600;
    letter-spacing: .04em;
}
.sig-yes { background: #d4edda; color: #1a5c32; }
.sig-no  { background: #fde8e8; color: #7a2020; }
.sig-mar { background: #fff3cd; color: #6d4c00; }

.section-label {
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: var(--mid);
    margin-bottom: .4rem;
    margin-top: 1.2rem;
    border-bottom: 1px solid rgba(13,31,60,.08);
    padding-bottom: .3rem;
}

.upload-note { font-size: .82rem; color: var(--mid); margin-top: -.4rem; margin-bottom: .8rem; }
.stDataFrame { border-radius: 8px; overflow: hidden; }
.footer {
    text-align: center;
    font-size: .75rem;
    color: var(--mid);
    padding: 1.2rem 0 .4rem;
    border-top: 1px solid rgba(13,31,60,.1);
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## WiL Portal")
    st.markdown("**Women in Leadership in Economics**")
    st.markdown("---")
    section = st.radio(
        "Navigate",
        ["Upload STATA Data", "Data Explorer", "Indicators Tracker"],
        index=0,
    )

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>Women in Leadership in Economics</h1>
  <div><span class="badge">Research Data Portal</span></div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1 · Upload STATA
# ═══════════════════════════════════════════════════════════════════════════════
if section == "Upload STATA Data":
    st.markdown('<div class="card"><h3>Upload STATA Dataset (.dta)</h3></div>', unsafe_allow_html=True)
    st.markdown('<p class="upload-note">Upload a Stata <code>.dta</code> file from your survey, RCT, or baseline data collection. '
                'The portal will parse and display the dataset for exploratory review.</p>', unsafe_allow_html=True)

    if "wil_df" in st.session_state:
        col_info, col_btn = st.columns([4, 1])
        with col_info:
            st.info(
                f"📂 Currently loaded: **{st.session_state.get('wil_filename', 'dataset.dta')}** — "
                f"{st.session_state['wil_df'].shape[0]:,} rows × {st.session_state['wil_df'].shape[1]} columns"
            )
        with col_btn:
            st.markdown("<div style='padding-top:0.4rem'>", unsafe_allow_html=True)
            if st.button("🗑️ Remove Dataset", type="secondary", use_container_width=True):
                del st.session_state["wil_df"]
                del st.session_state["wil_filename"]
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("---")

    uploaded = st.file_uploader("Choose a .dta file", type=["dta"],
                                help="Supports Stata 13–19 format files. Max 200 MB.")

    if uploaded is not None:
        try:
            with st.spinner("Parsing STATA file…"):
                df = pd.read_stata(uploaded)
                st.session_state["wil_df"] = df
                st.session_state["wil_filename"] = uploaded.name

            st.success(f"✅ File loaded: **{uploaded.name}** — {df.shape[0]:,} rows × {df.shape[1]} columns")

            n_rows, n_cols = df.shape
            n_missing = int(df.isnull().sum().sum())
            n_complete = n_rows - df.isnull().any(axis=1).sum()
            pct_complete = round(100 * n_complete / n_rows, 1) if n_rows else 0

            st.markdown(f"""
            <div class="metric-row">
                <div class="metric-tile"><div class="val">{n_rows:,}</div><div class="lbl">Observations</div></div>
                <div class="metric-tile"><div class="val">{n_cols}</div><div class="lbl">Variables</div></div>
                <div class="metric-tile"><div class="val">{n_missing:,}</div><div class="lbl">Missing Cells</div></div>
                <div class="metric-tile"><div class="val">{pct_complete}%</div><div class="lbl">Complete Rows</div></div>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["Preview", "Variable Info", "Summary Stats"])

            with tab1:
                n_preview = st.slider("Rows to preview", 5, min(100, n_rows), 20)
                st.dataframe(df.head(n_preview), use_container_width=True)

            with tab2:
                vinfo = pd.DataFrame({
                    "Variable": df.columns,
                    "Dtype": [str(df[c].dtype) for c in df.columns],
                    "Non-Null": [df[c].notna().sum() for c in df.columns],
                    "Null": [df[c].isna().sum() for c in df.columns],
                    "Unique": [df[c].nunique() for c in df.columns],
                })
                st.dataframe(vinfo, use_container_width=True)

            with tab3:
                num_df = df.select_dtypes(include="number")
                if not num_df.empty:
                    st.dataframe(num_df.describe().round(3), use_container_width=True)
                else:
                    st.info("No numeric variables detected for summary statistics.")

            csv_buf = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download as CSV", data=csv_buf,
                               file_name=uploaded.name.replace(".dta", ".csv"), mime="text/csv")

        except Exception as e:
            st.error(f"Could not parse file: {e}")
            st.info("Make sure the file is a valid Stata `.dta` format (Stata 13–19).")
    else:
        if "wil_df" not in st.session_state:
            st.markdown("""
            <div class="card" style="text-align:center;padding:2.5rem;border:2px dashed #c9a84c">
                <div style="font-size:2.5rem">📂</div>
                <p style="color:#6b7a8d;margin-top:.6rem">
                    Drag & drop or browse to upload your <strong>.dta</strong> STATA file.<br>
                    <span style="font-size:.8rem">Survey data · Baseline indicators · RCT datasets</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2 · Data Explorer
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "Data Explorer":
    st.markdown('<div class="card"><h3>Data Explorer</h3></div>', unsafe_allow_html=True)

    if "wil_df" not in st.session_state:
        st.warning("No dataset loaded yet. Please upload a `.dta` file in the **Upload STATA Data** section first.")
    else:
        df = st.session_state["wil_df"]
        fname = st.session_state.get("wil_filename", "dataset.dta")
        st.success(f"📂 Using: **{fname}** — {df.shape[0]:,} rows × {df.shape[1]} columns")

        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Filter & Browse",
            "Distribution",
            "Cross-tab",
            "📊 Data Analysis",
            "🧪 RCT Analysis",
        ])

        # ── Tab 1: Filter & Browse ──────────────────────────────────────────
        with tab1:
            filter_col = st.selectbox("Filter by column (optional)", ["— None —"] + cat_cols)
            filtered_df = df.copy()
            if filter_col != "— None —":
                vals = df[filter_col].dropna().unique().tolist()
                chosen = st.multiselect(f"Select values for **{filter_col}**", vals, default=vals[:3])
                if chosen:
                    filtered_df = df[df[filter_col].isin(chosen)]
            st.markdown(f"<small style='color:#6b7a8d'>Showing {len(filtered_df):,} of {len(df):,} rows</small>",
                        unsafe_allow_html=True)
            n_preview = st.slider("Rows to show", 5, min(200, len(filtered_df)), 20, key="explorer_slider")
            st.dataframe(filtered_df.head(n_preview), use_container_width=True)
            csv_buf = filtered_df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download filtered CSV", data=csv_buf,
                               file_name=fname.replace(".dta", "_filtered.csv"), mime="text/csv")

        # ── Tab 2: Distribution ─────────────────────────────────────────────
        with tab2:
            col_a, col_b = st.columns(2)
            with col_a:
                if num_cols:
                    num_var = st.selectbox("Numeric variable", num_cols)
                    st.bar_chart(df[num_var].dropna().value_counts().sort_index())
                else:
                    st.info("No numeric columns found.")
            with col_b:
                if cat_cols:
                    cat_var = st.selectbox("Categorical variable", cat_cols)
                    vc = df[cat_var].value_counts().reset_index()
                    vc.columns = [cat_var, "Count"]
                    st.dataframe(vc, use_container_width=True, hide_index=True)
                else:
                    st.info("No categorical columns found.")

        # ── Tab 3: Cross-tab ────────────────────────────────────────────────
        with tab3:
            all_cols = df.columns.tolist()
            c1, c2 = st.columns(2)
            with c1:
                row_var = st.selectbox("Row variable", all_cols, index=0)
            with c2:
                col_var = st.selectbox("Column variable", all_cols, index=min(1, len(all_cols)-1))
            if row_var != col_var:
                ct = pd.crosstab(df[row_var], df[col_var])
                st.dataframe(ct, use_container_width=True)
            else:
                st.warning("Please select two different variables.")

        # ══════════════════════════════════════════════════════════════════════
        # Tab 4 · DATA ANALYSIS
        # ══════════════════════════════════════════════════════════════════════
        with tab4:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#0d1f3c,#1c3557);
                        border-radius:10px;padding:1.1rem 1.5rem;margin-bottom:1rem;">
              <span style="color:#c9a84c;font-family:'Playfair Display',serif;font-size:1.05rem;font-weight:700;">
                Descriptive Statistics & Analysis
              </span>
              <p style="color:rgba(255,255,255,.72);font-size:.82rem;margin:.25rem 0 0;">
                Compute mean, standard deviation, standard error, confidence intervals,
                normality tests, and pairwise correlations.
              </p>
            </div>
            """, unsafe_allow_html=True)

            if not num_cols:
                st.info("No numeric variables found in this dataset.")
            else:
                analysis_mode = st.radio(
                    "Analysis mode",
                    ["Single Variable", "Multi-Variable Summary", "Pairwise Correlation"],
                    horizontal=True,
                    key="da_mode"
                )

                # ── Single Variable ──────────────────────────────────────────
                if analysis_mode == "Single Variable":
                    col_l, col_r = st.columns([2, 2])
                    with col_l:
                        sel_var = st.selectbox("Choose variable", num_cols, key="da_single")
                    with col_r:
                        grp_by = st.selectbox("Group by (optional)", ["— None —"] + cat_cols, key="da_grp")

                    # Build series list
                    series_list, labels = [], []
                    if grp_by != "— None —":
                        for g in df[grp_by].dropna().unique():
                            s = df[df[grp_by] == g][sel_var].dropna()
                            if len(s) > 0:
                                series_list.append(s)
                                labels.append(str(g))
                    else:
                        series_list = [df[sel_var].dropna()]
                        labels = ["All observations"]

                    def describe_series(s, label):
                        q1, q3 = float(s.quantile(0.25)), float(s.quantile(0.75))
                        if len(s) >= 3:
                            if len(s) <= 5000:
                                _, norm_p = stats.shapiro(s)
                                norm_txt = f"p = {norm_p:.4f}"
                                norm_result = "Normal" if norm_p > 0.05 else "Non-normal"
                            else:
                                norm_txt = "n > 5,000 (skipped)"
                                norm_result = "—"
                        else:
                            norm_txt = "n < 3"
                            norm_result = "—"
                        return {
                            "Group": label,
                            "N": len(s),
                            "Mean": round(float(s.mean()), 4),
                            "Std Dev": round(float(s.std()), 4),
                            "Std Error": round(float(s.sem()), 4),
                            "Median": round(float(s.median()), 4),
                            "Min": round(float(s.min()), 4),
                            "Max": round(float(s.max()), 4),
                            "Q1 (25%)": round(q1, 4),
                            "Q3 (75%)": round(q3, 4),
                            "IQR": round(q3 - q1, 4),
                            "Skewness": round(float(s.skew()), 4),
                            "Kurtosis": round(float(s.kurtosis()), 4),
                            "Shapiro-Wilk": norm_txt,
                            "Normality": norm_result,
                        }

                    rows = [describe_series(s, lbl) for s, lbl in zip(series_list, labels)]

                    # Quick-glance tiles for first group
                    r = rows[0]
                    st.markdown(f"""
                    <div class="metric-row" style="margin-top:.8rem">
                      <div class="stat-tile"><div class="sval">{r['Mean']}</div><div class="slbl">Mean</div></div>
                      <div class="stat-tile"><div class="sval">{r['Std Dev']}</div><div class="slbl">Std Dev</div></div>
                      <div class="stat-tile"><div class="sval">{r['Std Error']}</div><div class="slbl">Std Error</div></div>
                      <div class="stat-tile"><div class="sval">{r['Median']}</div><div class="slbl">Median</div></div>
                      <div class="stat-tile"><div class="sval">{r['IQR']}</div><div class="slbl">IQR</div></div>
                      <div class="stat-tile"><div class="sval">{r['Skewness']}</div><div class="slbl">Skewness</div></div>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown('<p class="section-label">Full statistics table</p>', unsafe_allow_html=True)
                    stats_df = pd.DataFrame(rows)
                    st.dataframe(stats_df.set_index("Group").T, use_container_width=True)

                    # Confidence interval
                    st.markdown('<p class="section-label">Confidence interval for mean</p>', unsafe_allow_html=True)
                    ci_level = st.slider("Confidence level (%)", 80, 99, 95, key="ci_level") / 100
                    ci_rows = []
                    for s, lbl in zip(series_list, labels):
                        if len(s) >= 2:
                            ci = stats.t.interval(ci_level, df=len(s)-1, loc=s.mean(), scale=s.sem())
                            ci_rows.append({
                                "Group": lbl,
                                "N": len(s),
                                "Mean": round(s.mean(), 4),
                                f"CI Lower ({int(ci_level*100)}%)": round(ci[0], 4),
                                f"CI Upper ({int(ci_level*100)}%)": round(ci[1], 4),
                                "Margin of Error": round((ci[1]-ci[0])/2, 4),
                            })
                    if ci_rows:
                        st.dataframe(pd.DataFrame(ci_rows), use_container_width=True, hide_index=True)

                    st.markdown('<p class="section-label">Distribution chart</p>', unsafe_allow_html=True)
                    chart_data = pd.concat(
                        [s.rename(lbl) for s, lbl in zip(series_list, labels)], axis=1
                    )
                    st.bar_chart(chart_data.apply(lambda c: c.value_counts().sort_index()).fillna(0))

                # ── Multi-Variable Summary ────────────────────────────────────
                elif analysis_mode == "Multi-Variable Summary":
                    sel_vars = st.multiselect(
                        "Choose variables", num_cols,
                        default=num_cols[:min(5, len(num_cols))],
                        key="da_multi"
                    )
                    if sel_vars:
                        sub = df[sel_vars].dropna()

                        def q25(x): return x.quantile(.25)
                        def q75(x): return x.quantile(.75)

                        summary = sub.agg(["count", "mean", "std", "sem",
                                           "median", "min", "max",
                                           q25, q75, "skew", "kurt"]).T
                        summary.columns = ["N", "Mean", "Std Dev", "Std Error",
                                           "Median", "Min", "Max",
                                           "Q1 (25%)", "Q3 (75%)",
                                           "Skewness", "Kurtosis"]
                        summary["IQR"] = summary["Q3 (75%)"] - summary["Q1 (25%)"]
                        summary["CV (%)"] = (summary["Std Dev"] / summary["Mean"].abs() * 100).round(2)

                        st.dataframe(summary.round(4), use_container_width=True)
                        csv_buf = summary.round(4).to_csv().encode("utf-8")
                        st.download_button("⬇️ Download summary CSV", csv_buf,
                                           file_name="descriptive_stats.csv", mime="text/csv")

                        # Normality test for all selected
                        st.markdown('<p class="section-label">Shapiro-Wilk normality test</p>', unsafe_allow_html=True)
                        norm_rows = []
                        for v in sel_vars:
                            s = df[v].dropna()
                            if 3 <= len(s) <= 5000:
                                _, p = stats.shapiro(s)
                                norm_rows.append({
                                    "Variable": v,
                                    "N": len(s),
                                    "W-stat": round(_, 4),
                                    "p-value": round(p, 4),
                                    "Result": "✅ Normal" if p > 0.05 else "❌ Non-normal",
                                })
                            else:
                                norm_rows.append({"Variable": v, "N": len(s),
                                                  "W-stat": "—", "p-value": "—",
                                                  "Result": "n out of range"})
                        st.dataframe(pd.DataFrame(norm_rows), use_container_width=True, hide_index=True)
                    else:
                        st.info("Select at least one variable above.")

                # ── Pairwise Correlation ──────────────────────────────────────
                elif analysis_mode == "Pairwise Correlation":
                    sel_vars = st.multiselect(
                        "Choose variables", num_cols,
                        default=num_cols[:min(6, len(num_cols))],
                        key="da_corr"
                    )
                    corr_method = st.radio("Method", ["Pearson", "Spearman", "Kendall"], horizontal=True)

                    if len(sel_vars) >= 2:
                        corr_df = df[sel_vars].corr(method=corr_method.lower()).round(3)
                        st.markdown('<p class="section-label">Correlation matrix (colour-coded)</p>',
                                    unsafe_allow_html=True)
                        st.dataframe(
                            corr_df.style.background_gradient(cmap="RdYlGn", vmin=-1, vmax=1),
                            use_container_width=True
                        )

                        st.markdown('<p class="section-label">P-value matrix</p>', unsafe_allow_html=True)
                        pval_rows = {}
                        for v1 in sel_vars:
                            pval_rows[v1] = {}
                            for v2 in sel_vars:
                                pair = df[[v1, v2]].dropna()
                                if v1 == v2:
                                    pval_rows[v1][v2] = "—"
                                elif len(pair) >= 3:
                                    if corr_method == "Pearson":
                                        _, p = stats.pearsonr(pair[v1], pair[v2])
                                    elif corr_method == "Spearman":
                                        _, p = stats.spearmanr(pair[v1], pair[v2])
                                    else:
                                        _, p = stats.kendalltau(pair[v1], pair[v2])
                                    pval_rows[v1][v2] = round(p, 4)
                                else:
                                    pval_rows[v1][v2] = "n/a"
                        st.dataframe(pd.DataFrame(pval_rows), use_container_width=True)
                    else:
                        st.info("Select at least 2 variables for correlation analysis.")

        # ══════════════════════════════════════════════════════════════════════
        # Tab 5 · RCT ANALYSIS
        # ══════════════════════════════════════════════════════════════════════
        with tab5:
            st.markdown("""
            <div style="background:linear-gradient(135deg,#0d1f3c,#1a7a6e);
                        border-radius:10px;padding:1.2rem 1.6rem;margin-bottom:1.2rem;">
              <span style="color:#c9a84c;font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;">
                Randomised Control Trial Analysis
              </span>
              <p style="color:rgba(255,255,255,.75);font-size:.82rem;margin:.3rem 0 0;">
                Assign treatment / control groups, select outcomes, and run ATE estimation,
                randomisation balance checks, significance tests, and effect sizes.
              </p>
            </div>
            """, unsafe_allow_html=True)

            if not num_cols:
                st.info("No numeric variables found in this dataset.")
            else:
                # ── Setup ──────────────────────────────────────────────────
                st.markdown('<p class="section-label">Step 1 — RCT configuration</p>', unsafe_allow_html=True)
                col_s1, col_s2, col_s3 = st.columns(3)

                with col_s1:
                    treat_var = st.selectbox(
                        "Treatment indicator column",
                        ["— Select —"] + df.columns.tolist(),
                        help="Binary column: 1 = treated, 0 = control",
                        key="rct_treat"
                    )
                with col_s2:
                    outcome_vars = st.multiselect(
                        "Outcome variable(s)",
                        num_cols,
                        help="Endline / post-intervention outcomes",
                        key="rct_outcomes"
                    )
                with col_s3:
                    baseline_vars = st.multiselect(
                        "Baseline covariates (balance check)",
                        num_cols,
                        help="Pre-treatment characteristics",
                        key="rct_baseline"
                    )

                alpha = st.slider("Significance level (α)", 0.01, 0.10, 0.05,
                                  step=0.01, key="rct_alpha",
                                  help="Threshold for rejecting the null hypothesis")

                if treat_var == "— Select —":
                    st.info("👆 Select a binary treatment indicator column (0 = control, 1 = treated) to begin.")
                else:
                    treat_vals = df[treat_var].dropna().unique()
                    if set(treat_vals).issubset({0, 1, 0.0, 1.0, "0", "1"}):
                        treat_mask = df[treat_var].astype(float) == 1
                        ctrl_mask  = df[treat_var].astype(float) == 0
                        valid_treat = True
                    else:
                        st.warning(f"`{treat_var}` contains values {sorted(treat_vals)}. "
                                   "Treatment indicator must be binary (0/1).")
                        valid_treat = False

                    if valid_treat:
                        n_treat = int(treat_mask.sum())
                        n_ctrl  = int(ctrl_mask.sum())
                        n_total = n_treat + n_ctrl

                        # ── Sample tiles ──────────────────────────────────
                        st.markdown('<p class="section-label">Step 2 — Sample composition</p>',
                                    unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="metric-row">
                          <div class="metric-tile"><div class="val">{n_total:,}</div><div class="lbl">Total N</div></div>
                          <div class="metric-tile"><div class="val">{n_treat:,}</div><div class="lbl">Treated</div></div>
                          <div class="metric-tile"><div class="val">{n_ctrl:,}</div><div class="lbl">Control</div></div>
                          <div class="metric-tile"><div class="val">{round(100*n_treat/n_total,1)}%</div><div class="lbl">Treatment Share</div></div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── Balance Check ─────────────────────────────────
                        if baseline_vars:
                            st.markdown('<p class="section-label">Step 3 — Randomisation balance check (baseline covariates)</p>',
                                        unsafe_allow_html=True)
                            balance_rows = []
                            for bv in baseline_vars:
                                t_ser = df[treat_mask][bv].dropna()
                                c_ser = df[ctrl_mask][bv].dropna()
                                if len(t_ser) < 2 or len(c_ser) < 2:
                                    continue
                                t_stat, p_val = stats.ttest_ind(t_ser, c_ser, equal_var=False)
                                std_pool = np.sqrt((t_ser.var() + c_ser.var()) / 2)
                                smd = (t_ser.mean() - c_ser.mean()) / std_pool if std_pool > 0 else np.nan
                                balance_rows.append({
                                    "Variable": bv,
                                    "Mean (Treated)": round(float(t_ser.mean()), 4),
                                    "Mean (Control)": round(float(c_ser.mean()), 4),
                                    "Raw Difference": round(float(t_ser.mean() - c_ser.mean()), 4),
                                    "Std Mean Diff": round(float(smd), 4) if not np.isnan(smd) else "—",
                                    "t-stat": round(float(t_stat), 4),
                                    "p-value": round(float(p_val), 4),
                                    "Balance": "✅ Balanced" if p_val > alpha else "⚠️ Imbalanced",
                                })
                            if balance_rows:
                                bal_df = pd.DataFrame(balance_rows)
                                st.dataframe(bal_df, use_container_width=True, hide_index=True)
                                n_imbal = sum(1 for r in balance_rows if "⚠️" in r["Balance"])
                                if n_imbal == 0:
                                    st.success("✅ All baseline covariates are balanced across arms (p > α). "
                                               "Randomisation appears successful.")
                                else:
                                    st.warning(f"⚠️ {n_imbal} covariate(s) show imbalance (p ≤ α = {alpha}). "
                                               "Consider covariate-adjusted estimation or re-randomisation.")

                        # ── ATE / ITT Estimation ──────────────────────────
                        if outcome_vars:
                            st.markdown('<p class="section-label">Step 4 — Average Treatment Effect (ATE / ITT)</p>',
                                        unsafe_allow_html=True)
                            ate_rows = []
                            for ov in outcome_vars:
                                t_ser = df[treat_mask][ov].dropna()
                                c_ser = df[ctrl_mask][ov].dropna()
                                if len(t_ser) < 2 or len(c_ser) < 2:
                                    continue
                                ate = float(t_ser.mean() - c_ser.mean())
                                t_stat, p_val = stats.ttest_ind(t_ser, c_ser, equal_var=False)
                                se = float(np.sqrt(t_ser.var()/len(t_ser) + c_ser.var()/len(c_ser)))
                                z = stats.norm.ppf(1 - alpha/2)
                                ci_lo = ate - z * se
                                ci_hi = ate + z * se
                                std_pool = float(np.sqrt((t_ser.var() + c_ser.var()) / 2))
                                cohen_d = ate / std_pool if std_pool > 0 else np.nan
                                pct_chg = (ate / c_ser.mean() * 100) if c_ser.mean() != 0 else np.nan

                                if p_val <= alpha:
                                    sig_label = '<span class="sig-badge sig-yes">Significant ✓</span>'
                                elif p_val <= 0.10:
                                    sig_label = '<span class="sig-badge sig-mar">Marginal ~</span>'
                                else:
                                    sig_label = '<span class="sig-badge sig-no">Not Sig. ✗</span>'

                                ate_rows.append({
                                    "Outcome": ov,
                                    "N (T)": len(t_ser),
                                    "N (C)": len(c_ser),
                                    "Mean (T)": round(float(t_ser.mean()), 4),
                                    "Mean (C)": round(float(c_ser.mean()), 4),
                                    "ATE": round(ate, 4),
                                    "Std Error": round(se, 4),
                                    f"CI {int((1-alpha)*100)}% Lo": round(ci_lo, 4),
                                    f"CI {int((1-alpha)*100)}% Hi": round(ci_hi, 4),
                                    "t-stat": round(float(t_stat), 4),
                                    "p-value": round(float(p_val), 4),
                                    "Cohen's d": round(cohen_d, 4) if not np.isnan(cohen_d) else "—",
                                    "% Change": round(pct_chg, 2) if not np.isnan(pct_chg) else "—",
                                    "_sig_html": sig_label,
                                })

                            if ate_rows:
                                display_df = pd.DataFrame(ate_rows).drop(columns=["_sig_html"])
                                st.dataframe(display_df, use_container_width=True, hide_index=True)

                                # Visual significance cards
                                st.markdown('<p class="section-label">Significance summary</p>',
                                            unsafe_allow_html=True)
                                sig_html = ""
                                for r in ate_rows:
                                    direction = "↑" if r["ATE"] > 0 else "↓"
                                    sig_html += f"""
                                    <div style="background:var(--white);border:1px solid rgba(13,31,60,.09);
                                                border-radius:8px;padding:.85rem 1.2rem;margin-bottom:.6rem;
                                                display:flex;justify-content:space-between;align-items:center;
                                                flex-wrap:wrap;gap:.4rem;">
                                      <div>
                                        <strong style="color:var(--navy)">{r['Outcome']}</strong>
                                        <span style="color:var(--mid);font-size:.8rem;margin-left:.6rem">
                                          ATE = {r['ATE']} {direction} &nbsp;|&nbsp;
                                          p = {r['p-value']} &nbsp;|&nbsp;
                                          Cohen's d = {r["Cohen's d"]} &nbsp;|&nbsp;
                                          % Change = {r["% Change"]}%
                                        </span>
                                      </div>
                                      {r['_sig_html']}
                                    </div>
                                    """
                                st.markdown(sig_html, unsafe_allow_html=True)

                                csv_buf = display_df.to_csv(index=False).encode("utf-8")
                                st.download_button("⬇️ Download ATE results CSV", csv_buf,
                                                   file_name="rct_ate_results.csv", mime="text/csv")

                        # ── Non-parametric test ───────────────────────────
                        if outcome_vars:
                            with st.expander("🔬 Non-parametric test — Mann-Whitney U"):
                                st.markdown("Robust alternative when outcome distributions deviate from normality.")
                                mw_rows = []
                                for ov in outcome_vars:
                                    t_ser = df[treat_mask][ov].dropna()
                                    c_ser = df[ctrl_mask][ov].dropna()
                                    if len(t_ser) < 2 or len(c_ser) < 2:
                                        continue
                                    u_stat, p_val = stats.mannwhitneyu(t_ser, c_ser, alternative="two-sided")
                                    mw_rows.append({
                                        "Outcome": ov,
                                        "Median (T)": round(float(t_ser.median()), 4),
                                        "Median (C)": round(float(c_ser.median()), 4),
                                        "Median Diff": round(float(t_ser.median() - c_ser.median()), 4),
                                        "U-statistic": round(float(u_stat), 2),
                                        "p-value": round(float(p_val), 4),
                                        "Significant": "Yes ✓" if p_val <= alpha else "No ✗",
                                    })
                                if mw_rows:
                                    st.dataframe(pd.DataFrame(mw_rows), use_container_width=True, hide_index=True)

                        # ── Attrition / missing check ─────────────────────
                        if outcome_vars:
                            with st.expander("📋 Attrition check (missing outcomes by arm)"):
                                st.markdown("Tests whether missingness in outcomes is differential across arms, "
                                            "which could bias ATE estimates.")
                                attr_rows = []
                                for ov in outcome_vars:
                                    miss_t = df[treat_mask][ov].isna().sum()
                                    miss_c = df[ctrl_mask][ov].isna().sum()
                                    pct_t = round(100 * miss_t / n_treat, 2) if n_treat else 0
                                    pct_c = round(100 * miss_c / n_ctrl, 2) if n_ctrl else 0
                                    obs_t = df[treat_mask][ov].notna().astype(int)
                                    obs_c = df[ctrl_mask][ov].notna().astype(int)
                                    if obs_t.sum() + obs_c.sum() > 0:
                                        t_stat, p_val = stats.ttest_ind(obs_t, obs_c)
                                    else:
                                        t_stat, p_val = np.nan, np.nan
                                    attr_rows.append({
                                        "Outcome": ov,
                                        "Missing (T)": f"{miss_t} ({pct_t}%)",
                                        "Missing (C)": f"{miss_c} ({pct_c}%)",
                                        "p-value (diff)": round(float(p_val), 4) if not np.isnan(p_val) else "—",
                                        "Differential Attrition": "⚠️ Yes" if (not np.isnan(p_val) and p_val <= alpha) else "✅ No",
                                    })
                                if attr_rows:
                                    st.dataframe(pd.DataFrame(attr_rows), use_container_width=True, hide_index=True)

                        # ── Effect size guide ─────────────────────────────
                        with st.expander("📖 Interpretation guide"):
                            st.markdown("""
**Cohen's d — Effect Size**

| Value | Interpretation |
|---|---|
| < 0.2 | Negligible |
| 0.2 – 0.5 | Small |
| 0.5 – 0.8 | Medium |
| > 0.8 | Large |

**Key Terms**

- **ATE** — Average Treatment Effect: mean difference (treated − control)
- **ITT** — Intent-to-Treat: this analysis assumes full compliance with assignment
- **Std Mean Diff** — Standardised difference; values < 0.1 indicate good balance
- **CI** — Confidence interval using normal approximation
- **Mann-Whitney U** — Non-parametric test on medians; use when data are non-normal
- **Attrition check** — Differential missingness can introduce selection bias into ATE
""")

                        if not outcome_vars:
                            st.info("👆 Select outcome variable(s) above to run ATE estimation.")

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3 · Indicators Tracker
# ═══════════════════════════════════════════════════════════════════════════════
elif section == "Indicators Tracker":
    st.markdown('<div class="card"><h3>Baseline Indicators Tracker</h3>'
                '<p style="font-size:.88rem;color:#6b7a8d">Track the status of WiL\'s core gender-gap metrics across data collection waves.</p>'
                '</div>', unsafe_allow_html=True)

    indicators = pd.DataFrame({
        "Indicator": [
            "Share of women faculty in economics depts.",
            "Share of women in senior policy roles",
            "Women in editorial boards (econ journals)",
            "Women PhD enrolment rate",
            "Women at major economics conferences",
            "Mentorship programme reach",
        ],
        "Domain": ["Academia", "Policy", "Academia", "Academia", "Profession", "Programme"],
        "Data Source": ["Primary Survey", "Admin Data", "Desk Research", "UGC Records", "Event Registers", "Programme MIS"],
        "Baseline Status": ["In Progress", "Pending", "Complete", "Complete", "In Progress", "Not Started"],
        "Wave 1 Target": ["Q3 2025", "Q4 2025", "✓ Done", "✓ Done", "Q3 2025", "Q1 2026"],
    })

    status_color = {"Complete": "🟢", "In Progress": "🟡", "Pending": "🔴", "Not Started": "⚪"}
    indicators["Status"] = indicators["Baseline Status"].map(status_color) + " " + indicators["Baseline Status"]

    st.dataframe(
        indicators[["Indicator", "Domain", "Data Source", "Status", "Wave 1 Target"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")
    st.markdown("**Add / Update Indicator**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text_input("Indicator name")
    with col2:
        st.selectbox("Domain", ["Academia", "Policy", "Profession", "Programme"])
    with col3:
        st.selectbox("Status", ["Not Started", "Pending", "In Progress", "Complete"])
    st.button("➕ Add Indicator", type="primary")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">Women in Leadership in Economics</div>',
    unsafe_allow_html=True,
)
