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
        .metric-card {background:#fff;border:1px solid #dae5e0;border-radius:18px;padding:20px;min-height:126px;box-shadow:0 8px 22px rgba(12,55,43,.05);}
        .metric-icon {width:44px;height:44px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:#e5f8f0;font-size:1.4rem;float:left;margin-right:14px;}
        .metric-value {font-size:2rem;font-weight:900;color:#071b35;line-height:1;}
        .metric-label {font-weight:800;color:#071b35;margin-top:6px;}
        .metric-hint {font-size:.83rem;color:#687b8d;margin-top:7px;}
        .panel {background:#fff;border:1px solid #dae5e0;border-radius:18px;padding:18px;box-shadow:0 8px 22px rgba(12,55,43,.04);}
        .role-pill {display:inline-block;padding:4px 10px;border-radius:999px;background:#dff8ed;color:#006747;font-size:.78rem;font-weight:800;}
        .status-ok {color:#008f5a;font-weight:800;}
        .status-warn {color:#d98200;font-weight:800;}
        .status-bad {color:#d92d20;font-weight:800;}
        div[data-testid="stForm"] {background:#fff;border:1px solid #dce7e2;border-radius:18px;padding:18px;}
        .stButton>button, .stDownloadButton>button {border-radius:12px;font-weight:750;min-height:42px;}
        @media (max-width: 700px) {
          .block-container {padding:1rem .8rem 2rem;}
          .page-title {font-size:1.65rem;}
          .metric-card {min-height:112px;padding:15px;}
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
