import streamlit as st


def apply_styles() -> None:
    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] {background:#f4f8f6;}
        [data-testid="stHeader"] {background:rgba(244,248,246,.92);}
        [data-testid="stSidebar"] {background:linear-gradient(180deg,#003f37 0%,#00634f 100%);}
        [data-testid="stSidebar"] * {color:#fff;}
        [data-testid="stSidebar"] .stButton button {background:#00a86b;color:#fff;border:0;width:100%;}
        .block-container {max-width:1500px;padding-top:1.5rem;padding-bottom:3rem;}
        h1,h2,h3 {color:#071b35;letter-spacing:-.02em;}
        .brand {font-size:1.55rem;font-weight:900;line-height:1.05;color:#fff;margin:10px 0 4px;}
        .brand span {color:#28e0a0;}
        .eyebrow {font-size:.78rem;font-weight:800;letter-spacing:.16em;color:#008f5a;text-transform:uppercase;}
        .page-title {font-size:2.2rem;font-weight:850;color:#071b35;margin:.15rem 0 .1rem;}
        .page-subtitle {color:#52657b;margin-bottom:1rem;}
        .metric-card {background:#fff;border:1px solid #dae5e0;border-radius:18px;padding:18px;min-height:118px;box-shadow:0 8px 22px rgba(12,55,43,.05);overflow:hidden;}
        .metric-icon {width:44px;height:44px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:#e5f8f0;font-size:1.4rem;float:left;margin-right:14px;}
        .metric-icon .pro-icon {width:38px;height:30px;display:block;}
        .metric-icon .truck-photo {width:46px;height:38px;object-fit:contain;mix-blend-mode:multiply;}
        .metric-value {font-size:2rem;font-weight:900;color:#071b35;line-height:1;}
        .metric-label {font-weight:800;color:#071b35;margin-top:6px;overflow-wrap:anywhere;line-height:1.2;}
        .metric-hint {font-size:.83rem;color:#687b8d;margin-top:7px;}
        .panel {background:#fff;border:1px solid #dae5e0;border-radius:18px;padding:18px;box-shadow:0 8px 22px rgba(12,55,43,.04);}
        .role-pill {display:inline-block;padding:4px 10px;border-radius:999px;background:#dff8ed;color:#006747;font-size:.78rem;font-weight:800;}
        .status-ok {color:#008f5a;font-weight:800;}
        .status-warn {color:#d98200;font-weight:800;}
        .status-bad {color:#d92d20;font-weight:800;}
        .truck-card {background:#fff;border:1px solid #d9e6e1;border-radius:18px;padding:16px;margin:5px 0 14px;box-shadow:0 8px 24px rgba(0,74,57,.07);min-height:178px;}
        .truck-top {display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
        .truck-visual {display:flex;align-items:center;width:76px;height:50px;}
        .truck-visual .pro-icon {width:72px;height:48px;display:block;}
        .truck-visual .truck-photo {width:76px;height:50px;object-fit:contain;mix-blend-mode:multiply;}
        .pro-icon {width:32px;height:32px;display:block;flex:0 0 auto;}
        .equipment-row {display:grid;grid-template-columns:38px 1fr auto;align-items:center;gap:9px;margin:9px 0 5px;color:#071b35;}
        .equipment-row strong {font-size:.98rem;}
        .equipment-row span {font-size:.88rem;color:#52657b;font-weight:750;}
        .inspection-icon {display:flex;align-items:center;gap:10px;background:#f4f8f6;border:1px solid #dce8e3;border-radius:14px;padding:10px 12px;margin-bottom:8px;}
        .inspection-icon .pro-icon {width:38px;height:38px;}
        .inspection-icon strong {color:#071b35;font-size:1rem;}
        .score-box {display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:14px;padding:9px 14px;min-height:66px;}
        .score-box b {font-size:1.55rem;line-height:1;}.score-box span {font-size:.76rem;font-weight:850;margin-top:5px;text-transform:uppercase;}
        .score-box.ok {background:#dff8ed;color:#007c54;}.score-box.bad {background:#fff1dc;color:#a56800;}
        .ransa-tag {background:#007953;color:#fff;font-weight:900;font-size:.7rem;letter-spacing:.09em;padding:5px 8px;border-radius:6px;}
        .truck-plate {font-size:1.35rem;font-weight:900;color:#071b35;letter-spacing:.06em;margin:5px 0;}
        .truck-meta {display:flex;justify-content:space-between;color:#607286;font-size:.82rem;border-bottom:1px solid #edf2f0;padding-bottom:10px;}
        .fleet-status {display:flex;align-items:center;gap:7px;margin-top:11px;font-size:.84rem;font-weight:850;}
        .fleet-status span {width:9px;height:9px;border-radius:50%;display:inline-block;}
        .fleet-status.pending {color:#a56800}.fleet-status.pending span {background:#f5a623;}
        .fleet-status.ok {color:#007c54}.fleet-status.ok span {background:#00a86b;}
        .fleet-status.bad {color:#c62d25}.fleet-status.bad span {background:#e34b42;}
        div[data-testid="stForm"] {background:#fff;border:1px solid #dce7e2;border-radius:18px;padding:18px;}
        .stButton>button, .stDownloadButton>button {border-radius:12px;font-weight:750;min-height:42px;}
        @media (max-width: 700px) {
          .block-container {padding:1rem .8rem 2rem;}
          .page-title {font-size:1.65rem;}
          .metric-card {min-height:112px;padding:15px;}
        }
        @media (min-width: 701px) and (max-width: 1200px) {
          .metric-card {padding:14px;min-height:126px;}
          .metric-icon {float:none;margin:0 0 8px 0;}
          .metric-value {font-size:1.7rem;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon: str, value, label: str, hint: str = "") -> None:
    st.markdown(
        f"""<div class="metric-card"><div class="metric-icon">{icon}</div>
        <div class="metric-value">{value}</div><div class="metric-label">{label}</div>
        <div class="metric-hint">{hint}</div></div>""",
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="eyebrow">{kicker}</div><div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )
