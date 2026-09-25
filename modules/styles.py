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
        .block-container {width:100%;max-width:1500px;padding:1.5rem clamp(1rem,2.5vw,2.5rem) 3rem;box-sizing:border-box;}
        [data-testid="stMain"], [data-testid="stMainBlockContainer"] {min-width:0;max-width:100%;}
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {min-width:0;}
        [data-testid="stPlotlyChart"] {max-width:100%;overflow:hidden;}
        [data-testid="stImage"] img {display:block;max-width:100%;height:auto;object-fit:contain;}
        .truck-photo,.pro-icon,.kaironix-symbol {max-width:100%;height:auto;object-fit:contain;}
        h1,h2,h3 {color:#071b35;letter-spacing:-.02em;}
        .brand-wrap {display:flex;align-items:center;gap:11px;margin:10px 0 5px;}
        .brand-wrap .kaironix-symbol {width:48px;height:48px;flex:0 0 48px;}
        .brand {font-size:1.5rem;font-weight:900;line-height:1.05;color:#fff;}
        .brand span {color:#28e0a0;}
        .login-symbol {display:flex;justify-content:center;margin-bottom:10px;}
        .login-symbol .kaironix-symbol {width:72px;height:72px;filter:drop-shadow(0 8px 14px rgba(0,80,60,.16));}
        [data-testid="stAppViewContainer"]:has(.login-marker) .block-container {max-width:1420px;padding-top:1.2rem;}
        [data-testid="stAppViewContainer"]:has(.login-marker) [data-testid="stHeader"] {background:transparent;}
        [data-testid="stAppViewContainer"]:has(.login-marker) {background:radial-gradient(circle at 8% 12%,rgba(0,202,146,.24),transparent 24%),radial-gradient(circle at 92% 82%,rgba(0,159,115,.22),transparent 26%),linear-gradient(135deg,#04192c 0%,#06213a 48%,#003d38 100%);min-height:100vh;}
        [data-testid="stAppViewContainer"]:has(.login-marker)::before {content:"";position:fixed;inset:0;pointer-events:none;background-image:linear-gradient(rgba(68,221,175,.045) 1px,transparent 1px),linear-gradient(90deg,rgba(68,221,175,.045) 1px,transparent 1px);background-size:64px 64px;}
        .login-hero {min-height:690px;border-radius:26px;background-size:cover;background-position:center;position:relative;overflow:hidden;box-shadow:0 20px 48px rgba(3,35,38,.18);}
        .login-hero-copy {position:absolute;left:42px;top:42px;max-width:470px;color:#fff;}
        .login-hero-copy>span {font-size:.72rem;letter-spacing:.2em;font-weight:850;color:#6ce9ba;}
        .login-hero-copy h2 {font-size:2.65rem;line-height:1.08;color:#fff;margin:18px 0 16px;letter-spacing:-.035em;}
        .login-hero-copy h2 em {font-style:normal;color:#45dda5;}
        .login-hero-copy p {font-size:1rem;line-height:1.55;color:#deeee9;max-width:410px;}
        .login-hero-footer {position:absolute;left:42px;bottom:35px;display:flex;flex-direction:column;color:#fff;letter-spacing:.08em;}
        .login-hero-footer small {color:#a9c9c0;margin-top:4px;}
        .login-brand {text-align:center;margin:60px 0 22px;}
        .login-brand .login-symbol {margin-bottom:4px}.login-brand .kaironix-symbol {width:78px;height:78px;}
        .login-brand h1 {font-size:2.55rem;margin:0;color:#071b35;line-height:1;}
        .login-product {font-size:1.55rem;font-weight:900;color:#071b35;margin-top:7px;letter-spacing:.02em}.login-product b {color:#00a86b;}
        .login-brand p {color:#607286;margin:10px 0 0;}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] {max-width:480px;margin:0 auto;padding:24px;border-radius:20px;box-shadow:0 12px 30px rgba(7,27,53,.08);}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] button {background:linear-gradient(90deg,#008f68,#00b577);border:0;color:#fff;}
        .login-secure {text-align:center;color:#607286;font-size:.8rem;margin:18px 0 14px;}.login-pilot {text-align:center;color:#008f68;font-size:.8rem;font-weight:850;}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] {width:100%;max-width:590px;margin:72px auto 0;padding:0 34px 30px;box-sizing:border-box;border:1px solid rgba(55,232,178,.52);border-radius:25px;background:linear-gradient(180deg,rgba(4,44,56,.96),rgba(3,25,47,.97));box-shadow:0 28px 70px rgba(0,0,0,.38);overflow:hidden;}
        .dark-login-brand {display:flex;align-items:center;justify-content:center;gap:16px;margin:0 -34px 28px;padding:24px 28px 20px;background:linear-gradient(90deg,rgba(0,130,96,.32),rgba(3,28,50,.18));border-bottom:1px solid rgba(70,218,176,.23);}
        .dark-login-brand>div:last-child {min-width:0;white-space:nowrap;}
        .dark-login-brand .login-symbol {margin:0}.dark-login-brand .kaironix-symbol {width:62px;height:62px;}
        .dark-login-brand h1 {margin:0;color:#fff;font-size:2rem;line-height:1}.dark-login-brand p {margin:6px 0 0;color:#42e3ad;font-weight:900;letter-spacing:.22em;font-size:.85rem;}
        .dark-login-title {text-align:center;margin-bottom:24px}.dark-login-title h2 {color:#fff;font-size:1.55rem;margin:0 0 7px}.dark-login-title span {color:#90aabe;font-size:.78rem;}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] label {color:#dce8f2;font-weight:750;}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] div[data-baseweb="input"] {background:#061a31;border:1px solid #18d79c;border-radius:13px;box-shadow:0 0 0 3px rgba(24,215,156,.08);min-height:52px;}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] div[data-baseweb="input"]:has(input[type="password"]) {border-color:#8796ff;box-shadow:0 0 0 3px rgba(135,150,255,.08);}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] div[data-baseweb="input"] {background:#fff!important;}
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] input {
          color:#071b35!important;
          -webkit-text-fill-color:#071b35!important;
          caret-color:#00a878!important;
          background:#fff!important;
          font-weight:700!important;
          opacity:1!important;
        }
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] input::placeholder {
          color:#718096!important;
          -webkit-text-fill-color:#718096!important;
          opacity:1!important;
        }
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] input:-webkit-autofill,
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] input:-webkit-autofill:hover,
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] input:-webkit-autofill:focus {
          -webkit-text-fill-color:#071b35!important;
          -webkit-box-shadow:0 0 0 1000px #fff inset!important;
          box-shadow:0 0 0 1000px #fff inset!important;
          caret-color:#00a878!important;
        }
        [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] button[kind="primaryFormSubmit"] {margin-top:12px;background:linear-gradient(90deg,#11d89c,#29efb4);color:#022334;border:0;border-radius:13px;min-height:54px;font-size:1.02rem;font-weight:900;box-shadow:0 12px 25px rgba(20,221,161,.20);}
        .dark-login-pilot {text-align:center;color:#79e8c5;font-size:.8rem;font-weight:800;margin-top:18px;letter-spacing:.03em;}
        .eyebrow {font-size:.78rem;font-weight:800;letter-spacing:.16em;color:#008f5a;text-transform:uppercase;}
        .page-title {font-size:2.2rem;font-weight:850;color:#071b35;margin:.15rem 0 .1rem;}
        .page-subtitle {color:#52657b;margin-bottom:1rem;}
        .metric-card {background:#fff;border:1px solid #dae5e0;border-radius:18px;padding:18px;min-height:145px;box-shadow:0 8px 22px rgba(12,55,43,.05);overflow:hidden;display:flex;flex-direction:column;justify-content:center;}
        .metric-main {display:grid;grid-template-columns:54px minmax(0,1fr);gap:13px;align-items:center;}
        .metric-copy {min-width:0;}
        .metric-icon {width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:#e5f8f0;font-size:1.45rem;margin:0;}
        .metric-icon .pro-icon {width:38px;height:30px;display:block;}
        .metric-icon .truck-photo {width:46px;height:38px;object-fit:contain;mix-blend-mode:multiply;}
        .metric-value {font-size:2rem;font-weight:900;color:#071b35;line-height:1;}
        .metric-label {font-size:.98rem;font-weight:850;color:#071b35;margin-top:7px;line-height:1.2;white-space:normal;}
        .metric-hint {font-size:.83rem;color:#687b8d;margin-top:13px;line-height:1.25;min-height:1.1em;}
        .panel {background:#fff;border:1px solid #dae5e0;border-radius:18px;padding:18px;box-shadow:0 8px 22px rgba(12,55,43,.04);}
        .role-pill {display:inline-block;padding:4px 10px;border-radius:999px;background:#dff8ed;color:#006747;font-size:.78rem;font-weight:800;}
        .status-ok {color:#008f5a;font-weight:800;}
        .status-warn {color:#d98200;font-weight:800;}
        .status-bad {color:#d92d20;font-weight:800;}
        .unit-profile-head {background:linear-gradient(135deg,#ffffff,#eaf8f2);border:1px solid #d3e7de;border-radius:22px;padding:20px;display:grid;grid-template-columns:110px minmax(0,1fr) auto;align-items:center;gap:20px;box-shadow:0 10px 28px rgba(0,72,53,.08);margin:12px 0 18px;}
        .unit-profile-truck {width:105px;height:74px;display:flex;align-items:center}.unit-profile-truck .truck-photo {width:105px;height:70px;object-fit:contain;mix-blend-mode:multiply}.unit-profile-head>div:nth-child(2)>span {font-size:.7rem;color:#008f68;font-weight:900;letter-spacing:.13em}.unit-profile-head h2 {font-size:2rem;margin:3px 0;color:#071b35}.unit-profile-head p {margin:0;color:#607286}
        .profile-mini-card {background:#fff;border:1px solid #dce8e3;border-radius:15px;padding:15px;min-height:105px;display:grid;grid-template-columns:38px 1fr;grid-template-rows:auto auto;align-items:center;box-shadow:0 6px 18px rgba(8,72,54,.05)}.profile-mini-card>span {grid-row:1/3;font-size:1.35rem}.profile-mini-card>b {font-size:1.35rem;color:#071b35}.profile-mini-card>small {color:#6d8091;font-size:.72rem;font-weight:750}
        .profile-item {background:#fff;border:1px solid #dce8e3;border-radius:16px;padding:15px;text-align:center;min-height:145px;box-shadow:0 7px 18px rgba(8,72,54,.05)}.profile-item>div {width:52px;height:52px;border-radius:14px;background:#e9f6f0;margin:0 auto 8px;display:flex;align-items:center;justify-content:center}.profile-item .pro-icon {width:42px;height:42px}.profile-item>span {display:block;color:#607286;font-size:.78rem;font-weight:800}.profile-item>b {display:block;color:#071b35;font-size:1.05rem;margin-top:5px}
        .unit-finding {background:#fff;border:1px solid #dce7e2;border-left:5px solid #f5a623;border-radius:14px;padding:14px 16px;margin:9px 0;box-shadow:0 5px 14px rgba(8,72,54,.04)}.unit-finding>div {display:flex;justify-content:space-between;gap:12px}.unit-finding>div b {color:#071b35}.unit-finding>div span {background:#fff3d8;color:#8a5b00;border-radius:999px;padding:4px 9px;font-size:.7rem;font-weight:850}.unit-finding p {color:#40576c;margin:8px 0}.unit-finding small {color:#718294}
        .truck-card {background:#fff;border:1px solid #d9e6e1;border-radius:18px;padding:16px;margin:5px 0 8px;box-shadow:0 8px 24px rgba(0,74,57,.07);min-height:178px;}
        .truck-top {display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;}
        .truck-visual {display:flex;align-items:center;width:76px;height:50px;}
        .truck-visual .pro-icon {width:72px;height:48px;display:block;}
        .truck-visual .truck-photo {width:76px;height:50px;object-fit:contain;mix-blend-mode:multiply;}
        .pro-icon {width:32px;height:32px;display:block;flex:0 0 auto;}
        .equipment-row {display:grid;grid-template-columns:38px 1fr auto;align-items:center;gap:9px;margin:9px 0 5px;color:#071b35;}
        .equipment-row strong {font-size:.98rem;}
        .equipment-row span {font-size:.88rem;color:#52657b;font-weight:750;}
        .inventory-card {position:relative;overflow:hidden;background:linear-gradient(145deg,#ffffff 0%,#f4faf7 100%);border:1px solid #d8e7e1;border-radius:18px;padding:17px;min-height:138px;display:grid;grid-template-columns:62px minmax(0,1fr);align-items:center;gap:14px;margin:7px 0;box-shadow:0 10px 26px rgba(8,72,54,.09);transition:transform .18s ease,box-shadow .18s ease;}
        .inventory-card::before {content:"";position:absolute;left:0;top:0;bottom:0;width:6px;background:#00b978}.inventory-card.cone::before {background:#ff7a00}.inventory-card.chock::before {background:#ffc21c}.inventory-card.firstaid::before {background:#eb3446}.inventory-card.extinguisher::before {background:#e72d25}
        .inventory-card:hover {transform:translateY(-2px);box-shadow:0 14px 30px rgba(8,72,54,.13)}
        .inventory-icon {width:60px;height:60px;border-radius:16px;background:linear-gradient(145deg,#eff9f5,#dff2ea);display:flex;align-items:center;justify-content:center;box-shadow:inset 0 0 0 1px rgba(0,111,79,.06),0 7px 15px rgba(7,48,38,.08);}
        .inventory-card.cone .inventory-icon {background:linear-gradient(145deg,#fff5e6,#ffe0b5)}.inventory-card.chock .inventory-icon {background:linear-gradient(145deg,#fff9db,#ffe990)}.inventory-card.firstaid .inventory-icon,.inventory-card.extinguisher .inventory-icon {background:linear-gradient(145deg,#fff0f1,#ffd6d9)}
        .inventory-icon .pro-icon {width:46px;height:46px;filter:drop-shadow(0 4px 4px rgba(4,22,32,.18))}.inventory-copy span {display:block;color:#486176;font-size:.86rem;font-weight:850}.inventory-copy b {display:block;color:#071b35;font-size:2.15rem;line-height:1;margin:7px 0 5px}.inventory-copy small {display:block;color:#718294;font-size:.72rem;line-height:1.2}.inventory-note {background:#e9f4ff;border:1px solid #d1e5f6;border-radius:12px;padding:10px 13px;color:#31516a;font-size:.78rem;margin-top:8px;}
        .equipment-card {background:#fff;border:1px solid #dce8e3;border-radius:15px;padding:12px 14px;margin:8px 0;box-shadow:0 5px 15px rgba(12,55,43,.035);}
        .equipment-card-head {display:grid;grid-template-columns:42px minmax(0,1fr) auto;align-items:center;gap:11px;}
        .equipment-card-icon {width:42px;height:42px;border-radius:11px;background:#f1f7f4;display:flex;align-items:center;justify-content:center;}
        .equipment-card-icon .pro-icon {width:31px;height:31px;}
        .equipment-card-head strong {display:block;color:#071b35;font-size:.96rem;}
        .equipment-card-head small {display:block;color:#718294;font-size:.72rem;margin-top:2px;}
        .equipment-numbers {text-align:right}.equipment-numbers b {display:block;color:#071b35;font-size:1rem}.equipment-numbers span {display:block;color:#c24135;font-size:.7rem;font-weight:800;margin-top:2px;}
        .equipment-track {height:7px;background:#e7eeeb;border-radius:999px;overflow:hidden;margin-top:10px;}
        .equipment-track span {display:block;height:100%;border-radius:999px}.equipment-track .good {background:#00a86b}.equipment-track .warning {background:#f5a623}.equipment-track .danger {background:#e34b42;}
        .alerts-section-title {display:flex;align-items:flex-end;justify-content:space-between;margin:28px 0 11px;border-top:1px solid #dce7e2;padding-top:22px;}
        .alerts-section-title span {color:#008f68;font-size:.72rem;font-weight:900;letter-spacing:.13em}.alerts-section-title h3 {font-size:1.45rem;margin:3px 0 0;}
        .alert-summary {background:#fff;border:1px solid #dce7e2;border-radius:15px;padding:15px 18px;display:flex;align-items:center;gap:12px;box-shadow:0 6px 18px rgba(12,55,43,.04);margin-bottom:10px;}
        .alert-summary b {font-size:1.65rem;line-height:1}.alert-summary span {font-size:.82rem;font-weight:800;color:#52657b}.alert-summary.red {border-left:5px solid #d92d20}.alert-summary.orange {border-left:5px solid #f5a623}.alert-summary.navy {border-left:5px solid #213c59;}
        .dashboard-alert {background:#fff;border:1px solid #dce7e2;border-left:6px solid #7e92a4;border-radius:15px;padding:13px 16px;margin:9px 0;display:grid;grid-template-columns:minmax(0,1.4fr) minmax(390px,1fr);align-items:center;gap:18px;box-shadow:0 6px 17px rgba(12,55,43,.04);}
        .dashboard-alert.critical {border-left-color:#d92d20}.dashboard-alert.high {border-left-color:#ed6a3a}.dashboard-alert.medium {border-left-color:#f5a623}.dashboard-alert.low {border-left-color:#4aa67b;}
        .dashboard-alert-main {display:grid;grid-template-columns:92px minmax(0,1fr);align-items:center;gap:14px}.dashboard-alert-plate {font-size:1.05rem;font-weight:950;color:#071b35;letter-spacing:.055em;}
        .dashboard-alert-copy strong {color:#008f68;font-size:.76rem;text-transform:uppercase;letter-spacing:.06em}.dashboard-alert-copy p {color:#40576c;font-size:.84rem;margin:4px 0 0;line-height:1.35;}
        .dashboard-alert-meta {display:flex;align-items:center;justify-content:flex-end;gap:12px;flex-wrap:wrap;color:#607286;font-size:.75rem}.dashboard-alert-meta b {color:#273f55;}
        .priority-badge,.overdue-badge {border-radius:999px;padding:5px 9px;background:#fff2d8;color:#8a5b00;font-size:.68rem;font-weight:900}.overdue-badge {background:#fde7e5;color:#b42318;}
        .alerts-empty {background:linear-gradient(135deg,#fff,#eef9f4);border:1px solid #d4e8df;border-radius:18px;padding:32px;text-align:center}.alerts-empty>div {width:52px;height:52px;display:flex;align-items:center;justify-content:center;border-radius:50%;background:#dff8ed;color:#008f68;font-size:1.5rem;font-weight:900;margin:0 auto 8px}.alerts-empty h3 {margin:4px 0}.alerts-empty p {color:#607286;margin:0;}
        .inspection-icon {display:flex;align-items:center;gap:10px;background:#f4f8f6;border:1px solid #dce8e3;border-radius:14px;padding:10px 12px;margin-bottom:8px;}
        .inspection-icon .pro-icon {width:38px;height:38px;}
        .inspection-icon strong {color:#071b35;font-size:1rem;}
        .score-box {display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:14px;padding:9px 14px;min-height:66px;}
        .score-box b {font-size:1.55rem;line-height:1;}.score-box span {font-size:.76rem;font-weight:850;margin-top:5px;text-transform:uppercase;}
        .score-box.ok {background:#dff8ed;color:#007c54;}.score-box.bad {background:#fff1dc;color:#a56800;}
        .findings-empty {background:linear-gradient(135deg,#ffffff 0%,#edf9f4 100%);border:1px solid #d4e8df;border-radius:22px;padding:42px 24px;text-align:center;box-shadow:0 10px 28px rgba(0,83,61,.06);margin-top:18px;}
        .findings-empty-icon {width:72px;height:72px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:0 auto 14px;background:#dff8ed;color:#008f68;font-size:2rem;font-weight:900;border:8px solid #f4fcf8;}
        .findings-empty h3 {margin:4px 0 8px}.findings-empty p {color:#607286;max-width:650px;margin:0 auto 20px;}
        .empty-flow {display:flex;justify-content:center;gap:10px;flex-wrap:wrap}.empty-flow span {background:#fff;border:1px solid #d6e6df;border-radius:999px;padding:7px 13px;color:#31516a;font-size:.82rem;font-weight:800;}
        .finding-card {background:#fff;border:1px solid #dce7e2;border-left:6px solid #7e92a4;border-radius:16px;padding:16px 18px;margin:10px 0;box-shadow:0 7px 18px rgba(12,55,43,.045);}
        .finding-card.low {border-left-color:#4aa67b}.finding-card.medium {border-left-color:#f5a623}.finding-card.high {border-left-color:#ed6a3a}.finding-card.critical {border-left-color:#d92d20;}
        .finding-head {display:flex;justify-content:space-between;align-items:center;gap:12px}.finding-head b {font-size:1.12rem;color:#071b35}.finding-id {color:#7b8d9e;font-size:.78rem;font-weight:800;margin-right:9px;}
        .criticality-pill,.state-pill {border-radius:999px;padding:5px 10px;background:#eef4f1;font-size:.73rem;font-weight:850;color:#304d62;}
        .finding-card.critical .criticality-pill {background:#fde7e5;color:#b42318}.finding-card.high .criticality-pill {background:#fff0e8;color:#b54708}.finding-card.medium .criticality-pill {background:#fff5d9;color:#8a5b00}.finding-card.low .criticality-pill {background:#e7f7ef;color:#08754f}
        .finding-category {font-size:.76rem;font-weight:850;color:#008f68;text-transform:uppercase;letter-spacing:.08em;margin:9px 0 3px}.finding-card p {color:#3e556b;margin:5px 0 13px;}
        .finding-footer {display:flex;gap:18px;align-items:center;flex-wrap:wrap;border-top:1px solid #edf2ef;padding-top:11px;color:#607286;font-size:.8rem}.finding-footer .state-pill {margin-left:auto;}
        .ransa-tag {background:#007953;color:#fff;font-weight:900;font-size:.7rem;letter-spacing:.09em;padding:5px 8px;border-radius:6px;}
        .truck-plate {font-size:1.35rem;font-weight:900;color:#071b35;letter-spacing:.06em;margin:5px 0;}
        .truck-meta {display:flex;justify-content:space-between;color:#607286;font-size:.82rem;border-bottom:1px solid #edf2f0;padding-bottom:10px;}
        .fleet-status {display:flex;align-items:center;gap:7px;margin-top:11px;font-size:.84rem;font-weight:850;}
        .fleet-status span {width:9px;height:9px;border-radius:50%;display:inline-block;}
        .fleet-status.pending {color:#a56800}.fleet-status.pending span {background:#f5a623;}
        .fleet-status.ok {color:#007c54}.fleet-status.ok span {background:#00a86b;}
        .fleet-status.bad {color:#c62d25}.fleet-status.bad span {background:#e34b42;}
        .fleet-status.workshop {color:#4256a5}.fleet-status.workshop span {background:#5266b4;}
        div[data-testid="stForm"] {background:#fff;border:1px solid #dce7e2;border-radius:18px;padding:18px;}
        .stButton>button, .stDownloadButton>button {border-radius:12px;font-weight:750;min-height:42px;}
        @media (max-width: 700px) {
          .block-container {padding:1rem .8rem 2rem;}
          [data-testid="stHorizontalBlock"] {flex-wrap:wrap;}
          [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {flex:1 1 100%;width:100%;min-width:0;}
          [data-testid="stPlotlyChart"], [data-testid="stPlotlyChart"] > div {width:100%;max-width:100%;}
          .metric-card,.inventory-card,.truck-card,.panel {width:100%;max-width:100%;box-sizing:border-box;}
          .page-title,.page-subtitle,.metric-label,.metric-hint,.truck-meta,.unit-profile-head p {overflow-wrap:anywhere;}
          .truck-photo {object-fit:contain;}
          .page-title {font-size:1.65rem;}
          .metric-card {min-height:132px;padding:15px;}
          .metric-main {grid-template-columns:48px minmax(0,1fr);gap:10px;}
          .metric-icon {width:48px;height:48px;}
          .unit-profile-head {grid-template-columns:72px minmax(0,1fr);gap:12px;padding:15px}.unit-profile-truck {width:70px;height:55px}.unit-profile-truck .truck-photo {width:70px;height:52px}.unit-profile-head>.fleet-status {grid-column:1/3;margin-top:0}.unit-profile-head h2 {font-size:1.55rem}.profile-mini-card {min-height:92px;padding:12px}.profile-item {min-height:125px;padding:12px}
          .inventory-card {grid-template-columns:48px minmax(0,1fr);padding:13px;min-height:112px;gap:10px}.inventory-icon {width:48px;height:48px}.inventory-icon .pro-icon {width:34px;height:34px}.inventory-copy b {font-size:1.7rem;}
          .equipment-card-head {grid-template-columns:38px minmax(0,1fr) auto;gap:8px}.equipment-card-icon {width:38px;height:38px}.equipment-numbers span {font-size:.65rem;}
          .dashboard-alert {grid-template-columns:1fr;gap:10px}.dashboard-alert-main {grid-template-columns:76px minmax(0,1fr)}.dashboard-alert-meta {justify-content:flex-start;border-top:1px solid #edf2ef;padding-top:9px;}
          .login-hero {min-height:260px;border-radius:18px;}
          .login-hero-copy {left:22px;top:24px;max-width:300px}.login-hero-copy>span {font-size:.6rem}.login-hero-copy h2 {font-size:1.7rem;margin:10px 0}.login-hero-copy p {display:none;}
          .login-hero-footer {left:22px;bottom:20px;font-size:.75rem;}
          .login-brand {margin:26px 0 16px}.login-brand h1 {font-size:2rem}.login-brand .kaironix-symbol {width:62px;height:62px;}
          [data-testid="stAppViewContainer"]:has(.login-marker) div[data-testid="stForm"] {width:min(100%,440px);margin:28px auto 0;padding:0 18px 24px;border-radius:20px;}
          .dark-login-brand {margin:0 -18px 24px;padding:18px 12px;gap:10px}.dark-login-brand h1 {font-size:clamp(1.3rem,6vw,1.7rem)}.dark-login-brand p {font-size:.72rem;letter-spacing:.12em}.dark-login-brand .kaironix-symbol {width:46px;height:46px;}
        }
        @media (min-width: 701px) and (max-width: 1200px) {
          .metric-card {padding:14px;min-height:140px;}
          .metric-main {grid-template-columns:48px minmax(0,1fr);gap:10px;}
          .metric-icon {width:48px;height:48px;}
          .metric-value {font-size:1.7rem;}
        }
        @media (max-width: 1000px) {
          .block-container {padding-left:1rem;padding-right:1rem;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def metric_card(icon: str, value, label: str, hint: str = "") -> None:
    st.markdown(
        f"""<div class="metric-card"><div class="metric-main">
        <div class="metric-icon">{icon}</div><div class="metric-copy">
        <div class="metric-value">{value}</div><div class="metric-label">{label}</div></div></div>
        <div class="metric-hint">{hint}</div></div>""",
        unsafe_allow_html=True,
    )


def page_header(kicker: str, title: str, subtitle: str) -> None:
    st.markdown(
        f'<div class="eyebrow">{kicker}</div><div class="page-title">{title}</div><div class="page-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )
