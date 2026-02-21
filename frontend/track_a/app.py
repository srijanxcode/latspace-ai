"""Track A Frontend — Intelligent Excel Parser (LatSpace styled)"""
import json
import os
import time

import httpx
import pandas as pd
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(
    page_title="LatSpace — Excel Parser",
    page_icon="🌿",
    layout="wide",
)

# ── Custom CSS matching LatSpace brand ────────────────────────────────────
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main background */
    .stApp {
        background-color: #f9fafb;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a1628;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #2d9e6b !important;
        font-size: 11px !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
    }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, #0a1628 0%, #1a2f4e 100%);
        padding: 48px 40px;
        border-radius: 12px;
        margin-bottom: 32px;
        border-left: 4px solid #2d9e6b;
    }
    .hero-banner h1 {
        color: #ffffff;
        font-size: 36px;
        font-weight: 800;
        margin: 0 0 8px 0;
        letter-spacing: -0.5px;
    }
    .hero-banner .tag {
        color: #2d9e6b;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 3px;
        margin-bottom: 12px;
    }
    .hero-banner p {
        color: #94a3b8;
        font-size: 16px;
        margin: 0;
        max-width: 600px;
    }

    /* Cards */
    .metric-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    }
    .metric-card .value {
        font-size: 36px;
        font-weight: 800;
        color: #0a1628;
    }
    .metric-card .label {
        font-size: 13px;
        color: #64748b;
        font-weight: 500;
        margin-top: 4px;
    }
    .metric-card.green .value { color: #2d9e6b; }
    .metric-card.red .value { color: #ef4444; }
    .metric-card.yellow .value { color: #f59e0b; }

    /* Section headers */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #0a1628;
        margin: 32px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #2d9e6b;
        display: inline-block;
    }

    /* Upload area */
    [data-testid="stFileUploader"] {
        background: #ffffff;
        border: 2px dashed #2d9e6b;
        border-radius: 10px;
        padding: 8px;
    }

    /* Primary button */
    .stButton > button[kind="primary"] {
        background-color: #2d9e6b !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        padding: 12px 24px !important;
        transition: background 0.2s !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #238a5a !important;
    }

    /* Info/warning/error boxes */
    .stAlert {
        border-radius: 8px !important;
    }

    /* Download button */
    .stDownloadButton > button {
        background-color: #0a1628 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #e2e8f0;
    }

    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 24px 0;">
        <div style="font-size:22px; font-weight:800; color:#ffffff; letter-spacing:-0.5px;">
            🌿 LatSpace
        </div>
        <div style="font-size:11px; color:#2d9e6b; font-weight:700; text-transform:uppercase; letter-spacing:2px; margin-top:4px;">
            AI × Sustainability
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Track A")
    st.markdown("<p style='color:#94a3b8; font-size:13px;'>Intelligent Excel Parser</p>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<p style='color:#2d9e6b; font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:2px;'>How It Works</p>", unsafe_allow_html=True)
    steps = [
        ("01", "Upload factory .xlsx file"),
        ("02", "AI detects headers & assets"),
        ("03", "Parameters mapped via Gemini"),
        ("04", "Values parsed & validated"),
        ("05", "Download clean JSON output"),
    ]
    for num, desc in steps:
        st.markdown(f"""
        <div style="display:flex; gap:12px; margin-bottom:12px; align-items:flex-start;">
            <div style="background:#2d9e6b; color:white; font-size:10px; font-weight:700;
                        border-radius:4px; padding:2px 6px; min-width:24px; text-align:center;">{num}</div>
            <div style="color:#cbd5e1; font-size:13px;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("<p style='color:#475569; font-size:12px;'>Powered by Google Gemini 1.5 Flash<br>One LLM call per sheet — cost efficient</p>", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="tag">AI × ESG Data Ingestion</div>
    <h1>Intelligent Excel Parser</h1>
    <p>Upload any factory spreadsheet — messy headers, mixed formats, multi-asset columns —
    and the AI agent maps it to the LatSpace parameter registry instantly.</p>
</div>
""", unsafe_allow_html=True)

# ── Upload & Options ───────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<div class='section-header'>Upload Data File</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=["xlsx"], label_visibility="collapsed")
    if uploaded:
        st.success(f"✅ Ready: **{uploaded.name}** ({uploaded.size / 1024:.1f} KB)")

with col2:
    st.markdown("<div class='section-header'>Options</div>", unsafe_allow_html=True)
    show_confidence = st.toggle("Highlight confidence levels", value=True)
    show_raw = st.toggle("Show raw JSON", value=False)
    st.markdown("""
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:12px; margin-top:12px;">
        <p style="color:#166534; font-size:13px; margin:0;">
        💡 <strong>Efficient:</strong> One Gemini API call per sheet maps all columns simultaneously.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if uploaded and st.button("🚀 Parse with AI", type="primary", use_container_width=True):
    with st.spinner("🤖 Gemini is analysing your file..."):
        start = time.time()
        try:
            response = httpx.post(
                f"{API_BASE}/api/track-a/parse",
                files={
                    "file": (
                        uploaded.name,
                        uploaded.getvalue(),
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                },
                timeout=60.0,
            )
            elapsed = time.time() - start

            if response.status_code == 200:
                result = response.json()

                # ── Metrics ────────────────────────────────────────────────
                st.markdown("<div class='section-header'>Results</div>", unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"""<div class="metric-card green">
                        <div class="value">{len(result['parsed_data'])}</div>
                        <div class="label">Parsed Cells</div></div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div class="metric-card yellow">
                        <div class="value">{len(result['unmapped_columns'])}</div>
                        <div class="label">Unmapped Columns</div></div>""", unsafe_allow_html=True)
                with c3:
                    st.markdown(f"""<div class="metric-card">
                        <div class="value">{len(result['warnings'])}</div>
                        <div class="label">Warnings</div></div>""", unsafe_allow_html=True)
                with c4:
                    st.markdown(f"""<div class="metric-card red">
                        <div class="value">{len(result.get('duplicate_flags', []))}</div>
                        <div class="label">Duplicates</div></div>""", unsafe_allow_html=True)

                st.markdown(f"<p style='color:#64748b; font-size:13px; margin-top:8px;'>⏱ Parsed in {elapsed:.1f}s</p>", unsafe_allow_html=True)

                # ── Parsed Data ────────────────────────────────────────────
                st.markdown("<div class='section-header'>Parsed Data</div>", unsafe_allow_html=True)
                if result["parsed_data"]:
                    df = pd.DataFrame(result["parsed_data"])

                    if show_confidence:
                        def _highlight(row):
                            color = {
                                "high":   "background-color: #d1fae5; color: #065f46",
                                "medium": "background-color: #fef3c7; color: #92400e",
                                "low":    "background-color: #fee2e2; color: #991b1b",
                            }.get(row["confidence"], "")
                            return [color] * len(row)
                        st.dataframe(df.style.apply(_highlight, axis=1), use_container_width=True, height=380)
                    else:
                        st.dataframe(df, use_container_width=True, height=380)

                    # Confidence breakdown
                    conf = df["confidence"].value_counts()
                    cc1, cc2, cc3 = st.columns(3)
                    cc1.markdown(f"""<div class="metric-card green"><div class="value">{conf.get('high',0)}</div><div class="label">🟢 High Confidence</div></div>""", unsafe_allow_html=True)
                    cc2.markdown(f"""<div class="metric-card yellow"><div class="value">{conf.get('medium',0)}</div><div class="label">🟡 Medium Confidence</div></div>""", unsafe_allow_html=True)
                    cc3.markdown(f"""<div class="metric-card red"><div class="value">{conf.get('low',0)}</div><div class="label">🔴 Low Confidence</div></div>""", unsafe_allow_html=True)

                # ── Unmapped ───────────────────────────────────────────────
                if result["unmapped_columns"]:
                    st.markdown("<div class='section-header'>Unmapped Columns</div>", unsafe_allow_html=True)
                    st.dataframe(pd.DataFrame(result["unmapped_columns"]), use_container_width=True)

                # ── Warnings ───────────────────────────────────────────────
                if result["warnings"]:
                    st.markdown("<div class='section-header'>Warnings</div>", unsafe_allow_html=True)
                    for w in result["warnings"]:
                        st.warning(w)

                # ── Duplicates ─────────────────────────────────────────────
                if result.get("duplicate_flags"):
                    st.markdown("<div class='section-header'>Duplicate Flags</div>", unsafe_allow_html=True)
                    for d in result["duplicate_flags"]:
                        st.error(d)

                # ── Download ───────────────────────────────────────────────
                st.divider()
                st.download_button(
                    label="⬇️ Download Clean JSON",
                    data=json.dumps(result, indent=2),
                    file_name=f"{uploaded.name.replace('.xlsx','')}_parsed.json",
                    mime="application/json",
                    use_container_width=True,
                )

                if show_raw:
                    st.markdown("<div class='section-header'>Raw JSON</div>", unsafe_allow_html=True)
                    st.json(result)

            else:
                st.error(f"❌ API error {response.status_code}: {response.text}")

        except httpx.ConnectError:
            st.error(f"❌ Cannot connect to backend at {API_BASE}. Is it running?")
        except Exception as e:
            st.error(f"❌ Error: {e}")