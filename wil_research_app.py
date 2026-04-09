import streamlit as st
import pandas as pd
import io
import os

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
.hero .sub {
    font-size: .9rem;
    color: rgba(255,255,255,.7);
    letter-spacing: .04em;
    text-transform: uppercase;
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
    st.markdown("---")
    st.markdown("**Principal Investigators**")
    st.markdown("• Subarna Banerjee *(Post-Doc Fellow)*")
    st.markdown("• Charity Troyer Moore *(Sci. Director)*")
    st.markdown("• Rohini Pande *(Faculty Director)*")
    st.markdown("• Simone Schaner *(Gender Lead)*")
    st.markdown("---")
    st.markdown("<div style='font-size:.75rem;opacity:.6'>© 2026</div>", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="sub">Inclusion Economics India Centre · IFMR</div>
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

    uploaded = st.file_uploader("Choose a .dta file", type=["dta"],
                                help="Supports Stata 13–19 format files. Max 200 MB.")

    if uploaded is not None:
        try:
            with st.spinner("Parsing STATA file…"):
                df = pd.read_stata(uploaded)

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
            st.download_button("⬇️ Download as CSV", data=csv_buf,
                               file_name=uploaded.name.replace(".dta", ".csv"), mime="text/csv")

        except Exception as e:
            st.error(f"Could not parse file: {e}")
            st.info("Make sure the file is a valid Stata `.dta` format (Stata 13–19).")
    else:
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
    st.markdown('<div class="card"><h3>Data Explorer</h3>'
                '<p style="color:#6b7a8d;font-size:.88rem">Upload a .dta file in the <em>Upload STATA Data</em> section first, '
                'then return here to explore variables and distributions.</p></div>',
                unsafe_allow_html=True)
    st.info("💡 Tip: Upload your STATA dataset first, then use this section to filter, group, and analyse variables relevant to gender representation tracking.")

    st.markdown('<div class="card"><h3>Suggested Analysis Workflows</h3></div>', unsafe_allow_html=True)
    workflows = {
        "Gender Gap Baseline": ["Compute share of women by institution type", "Cross-tab by seniority level & discipline", "Map missing values in demographic fields"],
        "Survey Quality Checks": ["Check skip-logic consistency (SurveyCTO exports)", "Flag outliers in continuous measures", "Review interviewer-level completion rates"],
        "RCT Balance Check": ["Compare treatment vs control on covariates", "Verify randomisation strata", "Test for attrition bias"],
    }
    cols = st.columns(3)
    for i, (title, steps) in enumerate(workflows.items()):
        with cols[i]:
            steps_html = "".join(f"<li>{s}</li>" for s in steps)
            st.markdown(f'<div class="card" style="min-height:160px"><h3>{title}</h3>'
                        f'<ul style="font-size:.83rem;color:#6b7a8d">{steps_html}</ul></div>',
                        unsafe_allow_html=True)

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
