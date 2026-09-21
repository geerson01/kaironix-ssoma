from __future__ import annotations

import base64
import calendar
from datetime import date, timedelta
from html import escape
from io import BytesIO
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

from modules import auth, database as db
from modules.styles import apply_styles, metric_card, page_header


MASTER_UNITS = [
    ("ATG", "BYL715"), ("FF", "BXN841"), ("ACC", "BFX947"),
    ("ACC", "BHC896"), ("ACC", "BHC897"), ("FF", "BXO712"),
    ("ACC", "BFO868"), ("FF", "BXN844"), ("ACC", "BHD755"),
    ("ACC", "BFP837"), ("ACC", "BHC807"), ("FF", "BXN910"),
    ("ACC", "BHC887"), ("FF", "BXN836"), ("ACC", "BFO900"),
    ("ACC", "BHC895"), ("ACC", "BHD713"), ("ACC", "BHC884"),
    ("FF", "BYJ739"), ("FF", "BYG813"), ("FF", "BYG741"),
    ("FF", "BYI783"), ("FF", "BYI781"), ("FF", "BYG838"),
    ("FF", "BYH875"), ("FF", "BYG742"), ("FF", "BYH813"),
    ("FF", "BYG833"),
]

MONTHS_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]


def kaironix_icon() -> str:
    return '''<svg class="kaironix-symbol" viewBox="0 0 72 72" role="img" aria-label="Símbolo Kaironix">
      <defs><linearGradient id="kxg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#28e0a0"/><stop offset="1" stop-color="#008f68"/></linearGradient></defs>
      <path d="M36 4 62 15v19c0 17-10 28-26 34C20 62 10 51 10 34V15z" fill="#071b35" stroke="url(#kxg)" stroke-width="3"/>
      <path d="M26 20v32M27 37l18-17M27 37l19 16" fill="none" stroke="#fff" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="26" cy="20" r="3.5" fill="#28e0a0"/><circle cx="45" cy="20" r="3.5" fill="#28e0a0"/><circle cx="46" cy="53" r="3.5" fill="#28e0a0"/>
    </svg>'''


@st.cache_data(show_spinner=False)
def ransa_truck_image() -> str:
    image_path = Path(__file__).with_name("camion_ransa.png")
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f'<img class="truck-photo" src="data:image/png;base64,{encoded}" alt="Camión RANSA">'


@st.cache_data(show_spinner=False)
def login_background_data() -> str:
    image_path = Path(__file__).with_name("login_logistica.webp")
    if not image_path.exists():
        return ""
    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:image/webp;base64,{encoded}"


def professional_icon(name: str) -> str:
    icons = {
        "truck": ransa_truck_image(),
        "cone": '''<svg class="pro-icon realistic-icon cone-real" viewBox="-6 -6 76 76" aria-label="Cono de seguridad">
          <defs><linearGradient id="coneBody" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ffad22"/><stop offset=".48" stop-color="#ff6b00"/><stop offset="1" stop-color="#d94700"/></linearGradient><linearGradient id="coneBase" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ff7b00"/><stop offset="1" stop-color="#b93600"/></linearGradient></defs>
          <ellipse cx="32" cy="57" rx="25" ry="4" fill="#0a1d2d" opacity=".18"/>
          <path d="M27 7h10l12 43H15z" fill="url(#coneBody)" stroke="#c64200" stroke-width="1.4"/>
          <path d="M20 29h24l3 10H17z" fill="#fff" stroke="#e9eef1" stroke-width="1"/>
          <path d="M26 10h4L20 48h-3z" fill="#ffd27a" opacity=".55"/>
          <rect x="7" y="48" width="50" height="9" rx="3.5" fill="url(#coneBase)" stroke="#a92e00" stroke-width="1.4"/>
          <path d="M13 51h38" stroke="#ffb04b" stroke-width="2" opacity=".65"/>
        </svg>''',
        "chock": '''<svg class="pro-icon realistic-icon" viewBox="0 0 64 64" aria-label="Tacos de rueda">
          <defs><linearGradient id="chockBody" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#33465e"/><stop offset=".55" stop-color="#111d2c"/><stop offset="1" stop-color="#050b12"/></linearGradient></defs>
          <ellipse cx="33" cy="55" rx="25" ry="4" fill="#071b35" opacity=".2"/>
          <path d="M8 51V35c15 0 25-10 32-27l16 43z" fill="url(#chockBody)" stroke="#02070d" stroke-width="2"/>
          <path d="M14 40l8-3 5 14H17zm15-10 8-8 11 29H36z" fill="#ffc21c" stroke="#d08a00" stroke-width="1"/>
          <path d="M11 47h41" stroke="#667b91" stroke-width="2" opacity=".7"/>
          <rect x="6" y="51" width="52" height="6" rx="2" fill="#070d15"/>
        </svg>''',
        "firstaid": '''<svg class="pro-icon realistic-icon" viewBox="0 0 64 64" aria-label="Botiquín">
          <defs><linearGradient id="kitBody" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ff6670"/><stop offset=".5" stop-color="#e33442"/><stop offset="1" stop-color="#a91323"/></linearGradient></defs>
          <ellipse cx="32" cy="57" rx="24" ry="4" fill="#071b35" opacity=".16"/>
          <path d="M23 17v-5c0-4 3-7 7-7h5c4 0 7 3 7 7v5" fill="none" stroke="#921020" stroke-width="5"/>
          <rect x="6" y="16" width="52" height="40" rx="8" fill="url(#kitBody)" stroke="#9f1422" stroke-width="1.6"/>
          <path d="M10 22c10-4 34-4 44 0" fill="none" stroke="#ff9299" stroke-width="2" opacity=".55"/>
          <rect x="27" y="25" width="11" height="23" rx="2" fill="#fff"/>
          <rect x="21" y="31" width="23" height="11" rx="2" fill="#fff"/>
          <path d="M11 51h42" stroke="#8e1020" stroke-width="2" opacity=".45"/>
        </svg>''',
        "extinguisher": '''<svg class="pro-icon realistic-icon extinguisher-real" viewBox="-24 -20 560 552" aria-label="Extintor">
          <defs>
            <linearGradient id="extRed" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#ff5b50"/><stop offset=".5" stop-color="#e2241b"/><stop offset="1" stop-color="#9f100c"/></linearGradient>
          </defs>
          <path fill="#17283a" d="M512 32c0-9.6-4.3-18.7-11.7-24.7S483.1-1.3 473.7.6l-160 32C301.5 35.1 292 44.3 289 56h-65V32c0-17.7-14.3-32-32-32h-32c-17.7 0-32 14.3-32 32v28.4C72.7 72.7 26.7 109.9 2.5 159.5c-5.8 11.9-.9 26.3 11.1 32.1s26.3.9 32.1-11.1C62 146.9 91.8 121.1 128 110v28.8C90.2 156.8 64 195.3 64 240v128h224V240c0-44.7-26.2-83.2-64-101.2V104h65c3 11.7 12.5 20.9 24.7 23.4l160 32c9.4 1.9 19.1-.6 26.6-6.6S512 137.6 512 128V32z"/>
          <path fill="url(#extRed)" d="M128 138.8C90.2 156.8 64 195.3 64 240v128h224V240c0-44.7-26.2-83.2-64-101.2H128zM288 448v-32H64v32c0 35.3 28.7 64 64 64h96c35.3 0 64-28.7 64-64z"/>
          <rect x="108" y="238" width="136" height="78" rx="12" fill="#fff" stroke="#cbd5db" stroke-width="6"/>
          <path d="M132 262h88M132 284h62" stroke="#e2241b" stroke-width="10" stroke-linecap="round"/>
          <path d="M108 168c-16 47-13 125-5 171" fill="none" stroke="#ff9a94" stroke-width="14" opacity=".55" stroke-linecap="round"/>
        </svg>''',
    }
    return icons[name]


LOGO_PATH = Path(__file__).with_name("kaironix_icon.svg")
st.set_page_config(page_title="Kaironix SSOMA 360", page_icon=str(LOGO_PATH), layout="wide", initial_sidebar_state="expanded")
apply_styles()


def excel_bytes(sheets: dict[str, pd.DataFrame]) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name[:31], index=False)
    return output.getvalue()


def normalize_dates(frame: pd.DataFrame, column: str = "fecha") -> pd.DataFrame:
    if not frame.empty and column in frame.columns:
        frame = frame.copy()
        frame[column] = pd.to_datetime(frame[column], errors="coerce")
    return frame


def login_screen() -> None:
    st.markdown('<span class="login-marker"></span>', unsafe_allow_html=True)
    left, access, right = st.columns([1, 1.05, 1])
    with access:
        if not auth.configured():
            st.error("El proyecto todavía no tiene configuradas las credenciales de Supabase.")
        with st.form("login_form"):
            st.markdown(
                f"""<div class="dark-login-brand"><div class="login-symbol">{kaironix_icon()}</div>
                <div><h1>Kaironix</h1><p>SSOMA 360</p></div></div>
                <div class="dark-login-title"><h2>Acceso al sistema</h2><span>Sistema protegido · Solo personal autorizado</span></div>""",
                unsafe_allow_html=True,
            )
            identifier = st.text_input(
                "Usuario",
                value="",
                placeholder="",
                autocomplete="off",
                key="login_username",
            )
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Ingresar", use_container_width=True, type="primary")
        if submitted:
            ok, message = auth.sign_in(identifier, password)
            if ok:
                st.rerun()
            st.error(message)
        st.markdown('<div class="dark-login-pilot">● Piloto · CBC Huachipa</div>', unsafe_allow_html=True)


def load_session_profile() -> dict:
    current = auth.current_auth()
    if not current:
        return {}
    if "profile" not in st.session_state:
        st.session_state.profile = db.get_profile(current.get("user_id", ""))
    return st.session_state.get("profile", {})


def sidebar(profile: dict) -> str:
    role = profile.get("rol", "Consulta")
    st.sidebar.markdown(f'<div class="brand-wrap">{kaironix_icon()}<div class="brand">Kaironix<br><span>SSOMA 360</span></div></div>', unsafe_allow_html=True)
    st.sidebar.caption("Piloto · CBC Huachipa")
    st.sidebar.markdown("---")
    pages = ["Inicio", "Unidades", "Nueva inspección", "Hallazgos", "Evidencias", "Reportes"]
    if role == "Administrador":
        pages.append("Usuarios")
    selected = st.sidebar.radio(
        "Navegación",
        pages,
        label_visibility="collapsed",
        key="main_navigation",
    )
    components.html(
        """
        <script>
        (() => {
          const doc = window.parent.document;
          const storage = window.parent.sessionStorage;
          const sidebarSelector = '[data-testid="stSidebar"]';
          const radioSelector = [
            sidebarSelector + ' [role="radio"]',
            sidebarSelector + ' [role="radiogroup"] label',
            sidebarSelector + ' [data-testid="stRadio"] label',
            sidebarSelector + ' input[type="radio"]'
          ].join(',');

          const ensureStyles = () => {
            if (doc.getElementById('kaironix-sidebar-motion')) return;
            const style = doc.createElement('style');
            style.id = 'kaironix-sidebar-motion';
            style.textContent = `
              [data-testid="stSidebar"] {
                transition: transform .28s ease, margin-left .28s ease !important;
              }
              body.kx-sidebar-hidden [data-testid="stSidebar"] {
                transform: translateX(-105%) !important;
                margin-left: calc(-1 * var(--kx-sidebar-width, 21rem)) !important;
              }
              #kx-sidebar-open {
                position: fixed; top: 76px; left: 12px; z-index: 999999;
                width: 42px; height: 42px; border: 0; border-radius: 11px;
                background: #005b49; color: white; font-size: 23px;
                box-shadow: 0 7px 18px rgba(0,55,43,.28); cursor: pointer;
                display: none; align-items: center; justify-content: center;
              }
              body.kx-sidebar-hidden #kx-sidebar-open { display: flex; }
              @media (max-width: 700px) {
                #kx-sidebar-open { top: 64px; left: 8px; width: 39px; height: 39px; }
              }
            `;
            doc.head.appendChild(style);
          };

          const ensureOpenButton = () => {
            let button = doc.getElementById('kx-sidebar-open');
            if (!button) {
              button = doc.createElement('button');
              button.id = 'kx-sidebar-open';
              button.type = 'button';
              button.title = 'Abrir menú';
              button.setAttribute('aria-label', 'Abrir menú');
              button.textContent = '☰';
              button.addEventListener('click', () => {
                doc.body.classList.remove('kx-sidebar-hidden');
                storage.removeItem('kx-sidebar-closed');
              });
              doc.body.appendChild(button);
            }
          };

          const hideSidebar = () => {
            const sidebar = doc.querySelector(sidebarSelector);
            if (!sidebar) return false;
            const width = sidebar.getBoundingClientRect().width;
            if (width > 20) {
              doc.documentElement.style.setProperty('--kx-sidebar-width', width + 'px');
            }
            doc.body.classList.add('kx-sidebar-hidden');
            storage.setItem('kx-sidebar-closed', '1');
            return true;
          };

          const requestClose = () => {
            storage.setItem('kx-sidebar-close-after-nav', '1');
            setTimeout(hideSidebar, 320);
          };

          const bindNavigation = () => {
            const controls = doc.querySelectorAll(radioSelector);
            controls.forEach((control) => {
              if (control.dataset.kxBound === '1') return;
              control.dataset.kxBound = '1';
              control.addEventListener('click', requestClose, false);
            });
            return controls.length > 0;
          };

          ensureStyles();
          ensureOpenButton();

          let attempts = 0;
          const initialize = () => {
            attempts += 1;
            bindNavigation();
            if (
              storage.getItem('kx-sidebar-close-after-nav') === '1'
              || storage.getItem('kx-sidebar-closed') === '1'
            ) {
              storage.removeItem('kx-sidebar-close-after-nav');
              hideSidebar();
            }
            if (attempts < 40) setTimeout(initialize, 150);
          };
          initialize();

          const observer = new MutationObserver(() => bindNavigation());
          observer.observe(doc.body, {childList: true, subtree: true});
        })();
        </script>
        """,
        height=0,
        width=0,
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{profile.get('nombre','Usuario')}**")
    st.sidebar.markdown(f'<span class="role-pill">{role}</span>', unsafe_allow_html=True)
    if st.sidebar.button("Cerrar sesión"):
        auth.sign_out()
        st.rerun()
    st.sidebar.markdown("<br><small>SEGURIDAD HOY.<br>OPERACIONES SIEMPRE.</small>", unsafe_allow_html=True)
    return selected


@st.cache_data(ttl=30, show_spinner=False)
def load_all():
    return (
        db.select("unidades", {"order": "placa.asc"}),
        db.select("inspecciones", {"order": "fecha.desc,created_at.desc"}),
        db.select("hallazgos", {"order": "fecha.desc,created_at.desc"}),
    )


def dashboard(unidades: pd.DataFrame, inspecciones: pd.DataFrame, hallazgos: pd.DataFrame) -> None:
    page_header("CONTROL PREVENTIVO DE FLOTA", "Panel general SSOMA", "La información se actualiza con cada inspección registrada.")
    today = pd.Timestamp.today().normalize()
    ins = normalize_dates(inspecciones)
    latest = pd.DataFrame()
    if not ins.empty:
        latest = ins.sort_values(["fecha", "created_at"], ascending=False).drop_duplicates("placa")

    open_h = (
        hallazgos[hallazgos["estado"] != "Subsanado"].copy()
        if not hallazgos.empty and "estado" in hallazgos
        else pd.DataFrame()
    )
    total = len(unidades)
    inspected = len(latest)
    conformes = int((latest.get("resultado", pd.Series(dtype=str)) == "Conforme").sum()) if not latest.empty else 0
    observadas = int((latest.get("resultado", pd.Series(dtype=str)) == "Observada").sum()) if not latest.empty else 0
    pending = max(total - inspected, 0)

    cols = st.columns(4)
    cards = [
        (professional_icon("truck"), total, "Unidades registradas", "Flota activa"),
        ("✓", conformes, "Conformes", "Última inspección"),
        ("⚠", observadas, "Observadas", "Requieren subsanación"),
        ("📋", inspected, "Inspeccionadas", f"{pending} pendientes"),
    ]
    for col, card in zip(cols, cards):
        with col:
            metric_card(*card)

    st.write("")
    c1, c2 = st.columns([1, 1.55])
    with c1:
        st.subheader("Cumplimiento general")
        values = [conformes, observadas, pending]
        fig = go.Figure(go.Pie(
            values=values if sum(values) else [1],
            labels=[
                f"Conformes ({conformes})",
                f"Observadas ({observadas})",
                f"Pendientes ({pending})",
            ],
            hole=.72,
            marker_colors=["#00c878", "#ff9d00", "#cbd9d5"],
            textinfo="value",
            textposition="inside",
            textfont=dict(size=17, color="#ffffff"),
        ))
        pct = round((conformes / total * 100), 1) if total else 0
        fig.add_annotation(
            text=f"<b>{pct}%</b><br><span style='font-size:12px'>cumplimiento</span>",
            showarrow=False,
            font_size=24,
        )
        fig.update_layout(
            height=340,
            margin=dict(l=5, r=5, t=5, b=5),
            legend=dict(orientation="h", y=-.08, font=dict(size=12)),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "staticPlot": True})

    with c2:
        st.subheader("Inventario de implementos registrado")
        st.caption(
            f"Cantidad física declarada en la última inspección de {inspected} unidades."
        )
        total_conos = (
            int(pd.to_numeric(latest.get("conos_cantidad"), errors="coerce").fillna(0).sum())
            if not latest.empty and "conos_cantidad" in latest else 0
        )
        total_tacos = (
            int(pd.to_numeric(latest.get("tacos_cantidad"), errors="coerce").fillna(0).sum())
            if not latest.empty and "tacos_cantidad" in latest else 0
        )
        total_botiquines = (
            int(
                latest["botiquin_estado"].fillna("").astype(str)
                .str.strip().str.lower().ne("no tiene").sum()
            )
            if not latest.empty and "botiquin_estado" in latest else 0
        )
        total_extintores = (
            int(latest["extintor_tiene"].fillna(False).astype(bool).sum())
            if not latest.empty and "extintor_tiene" in latest else 0
        )
        inventory = [
            ("cone", total_conos, "Conos", "unidades físicas registradas"),
            ("chock", total_tacos, "Tacos", "unidades físicas registradas"),
            ("firstaid", total_botiquines, "Botiquines", "camiones equipados"),
            ("extinguisher", total_extintores, "Extintores", "camiones equipados"),
        ]
        for row_start in range(0, len(inventory), 2):
            inv_cols = st.columns(2)
            for inv_col, (icon_name, quantity, label, unit_label) in zip(
                inv_cols, inventory[row_start:row_start + 2]
            ):
                with inv_col:
                    st.markdown(
                        f"""<div class="inventory-card {icon_name}">
                          <div class="inventory-icon">{professional_icon(icon_name)}</div>
                          <div class="inventory-copy">
                            <span>{label}</span>
                            <b>{quantity}</b>
                            <small>{unit_label}</small>
                          </div>
                        </div>""",
                        unsafe_allow_html=True,
                    )
        st.markdown(
            f'<div class="inventory-note">Base del conteo: última inspección de <b>{inspected}</b> unidades, sin duplicar placas.</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="alerts-section-title"><div><span>CENTRO PREVENTIVO</span><h3>Alertas y acciones prioritarias</h3></div></div>', unsafe_allow_html=True)
    if open_h.empty:
        st.markdown(
            '<div class="alerts-empty"><div>✓</div><h3>Sin alertas abiertas</h3><p>La flota no registra acciones pendientes.</p></div>',
            unsafe_allow_html=True,
        )
    else:
        alert_view = open_h.copy()
        alert_view["fecha_compromiso_dt"] = pd.to_datetime(
            alert_view.get("fecha_compromiso"), errors="coerce"
        )
        priority = {"Crítica": 0, "Alta": 1, "Media": 2, "Baja": 3}
        alert_view["_priority"] = alert_view.get(
            "criticidad", pd.Series("Baja", index=alert_view.index)
        ).map(priority).fillna(4)
        alert_view["_overdue"] = (
            alert_view["fecha_compromiso_dt"].notna()
            & (alert_view["fecha_compromiso_dt"] < today)
        )
        alert_view = alert_view.sort_values(
            ["_overdue", "_priority", "fecha_compromiso_dt"],
            ascending=[False, True, True],
        )
        critical_count = int(alert_view.get("criticidad", pd.Series(dtype=str)).isin(["Crítica", "Alta"]).sum())
        overdue_count = int(alert_view["_overdue"].sum())
        a1, a2, a3 = st.columns(3)
        with a1:
            st.markdown(f'<div class="alert-summary red"><b>{len(alert_view)}</b><span>Hallazgos abiertos</span></div>', unsafe_allow_html=True)
        with a2:
            st.markdown(f'<div class="alert-summary orange"><b>{critical_count}</b><span>Alta prioridad</span></div>', unsafe_allow_html=True)
        with a3:
            st.markdown(f'<div class="alert-summary navy"><b>{overdue_count}</b><span>Fuera de plazo</span></div>', unsafe_allow_html=True)

        for _, row in alert_view.head(6).iterrows():
            criticidad = str(row.get("criticidad", "Baja"))
            css_level = {"Crítica": "critical", "Alta": "high", "Media": "medium", "Baja": "low"}.get(criticidad, "low")
            due = row.get("fecha_compromiso_dt")
            due_text = due.strftime("%d/%m/%Y") if pd.notna(due) else "Sin fecha"
            overdue_badge = '<span class="overdue-badge">VENCIDA</span>' if bool(row.get("_overdue")) else ""
            st.markdown(
                f"""<div class="dashboard-alert {css_level}">
                  <div class="dashboard-alert-main">
                    <div class="dashboard-alert-plate">{escape(str(row.get("placa", "")))}</div>
                    <div class="dashboard-alert-copy">
                      <strong>{escape(str(row.get("categoria", "Hallazgo")))}</strong>
                      <p>{escape(str(row.get("descripcion", "")))}</p>
                    </div>
                  </div>
                  <div class="dashboard-alert-meta">
                    <span class="priority-badge">{escape(criticidad)}</span>
                    <span>Responsable: <b>{escape(str(row.get("responsable") or "Sin asignar"))}</b></span>
                    <span>Compromiso: <b>{due_text}</b></span>{overdue_badge}
                  </div>
                </div>""",
                unsafe_allow_html=True,
            )
        if len(alert_view) > 6:
            st.caption(f"Se muestran 6 alertas prioritarias de {len(alert_view)} abiertas. Revisa el módulo Hallazgos para ver todas.")

    st.download_button(
        "⬇ Exportar información a Excel",
        excel_bytes({"Unidades": unidades, "Inspecciones": inspecciones, "Hallazgos": hallazgos}),
        "reporte_ssoma_360.xlsx",
        use_container_width=False,
    )

def units_page(unidades: pd.DataFrame, inspecciones: pd.DataFrame, hallazgos: pd.DataFrame, can_edit: bool, is_admin: bool) -> None:
    page_header("MAESTRO DE FLOTA", "Unidades RANSA", "Consulta las placas, tipo de unidad y estado de su última inspección.")

    registered = set(unidades.get("placa", pd.Series(dtype=str)).astype(str).str.upper()) if not unidades.empty else set()
    missing = [(tipo, placa) for tipo, placa in MASTER_UNITS if placa not in registered]
    if is_admin and missing:
        st.info(f"Hay {len(missing)} unidades del maestro inicial pendientes de cargar.")
        if st.button("🚛 Cargar maestro de 28 unidades RANSA", type="primary"):
            failures = []
            for tipo, placa in missing:
                ok, msg = db.insert("unidades", {
                    "placa": placa, "tipo": tipo, "empresa": "RANSA",
                    "agencia": "Huachipa", "estado": "Activo",
                    "created_by": auth.current_auth().get("user_id"),
                })
                if not ok:
                    failures.append(f"{placa}: {msg}")
            load_all.clear()
            if failures:
                st.error("No se pudieron cargar algunas placas: " + " | ".join(failures[:3]))
            else:
                st.success("Maestro de unidades cargado correctamente.")
                st.rerun()

    latest_status: dict[str, str] = {}
    if not inspecciones.empty and "placa" in inspecciones:
        ordered = inspecciones.copy()
        ordered["fecha"] = pd.to_datetime(ordered["fecha"], errors="coerce")
        ordered = ordered.sort_values(["fecha", "created_at"], ascending=False).drop_duplicates("placa")
        latest_status = dict(zip(ordered["placa"], ordered["resultado"]))

    selected_plate = st.session_state.get("selected_unit_plate")
    if selected_plate:
        unit_rows = unidades[
            unidades["placa"].fillna("").astype(str).str.upper() == str(selected_plate).upper()
        ]
        if unit_rows.empty:
            st.session_state.pop("selected_unit_plate", None)
            st.rerun()
        unit_detail = unit_rows.iloc[0]
        plate_inspections = (
            inspecciones[
                inspecciones["placa"].fillna("").astype(str).str.upper() == str(selected_plate).upper()
            ].copy()
            if not inspecciones.empty and "placa" in inspecciones else pd.DataFrame()
        )
        if not plate_inspections.empty:
            plate_inspections["fecha_dt"] = pd.to_datetime(
                plate_inspections["fecha"], errors="coerce"
            )
            plate_inspections = plate_inspections.sort_values(
                ["fecha_dt", "created_at"], ascending=False
            )
        plate_findings = (
            hallazgos[
                hallazgos["placa"].fillna("").astype(str).str.upper() == str(selected_plate).upper()
            ].copy()
            if not hallazgos.empty and "placa" in hallazgos else pd.DataFrame()
        )

        if st.button("← Volver a la flota", key="back_to_fleet"):
            st.session_state.pop("selected_unit_plate", None)
            st.rerun()

        current_status = latest_status.get(str(selected_plate), "Pendiente")
        status_css = {"Conforme": "ok", "Observada": "bad", "Pendiente": "pending"}.get(current_status, "pending")
        st.markdown(
            f"""<div class="unit-profile-head">
              <div class="unit-profile-truck">{professional_icon("truck")}</div>
              <div><span>FICHA DE TRAZABILIDAD</span><h2>{escape(str(selected_plate))}</h2>
              <p>{escape(str(unit_detail.get("tipo", "-")))} · {escape(str(unit_detail.get("empresa", "RANSA")))} · {escape(str(unit_detail.get("agencia", "Huachipa")))}</p></div>
              <div class="fleet-status {status_css}"><span></span>{current_status}</div>
            </div>""",
            unsafe_allow_html=True,
        )

        if plate_inspections.empty:
            st.info("Esta unidad todavía no tiene inspecciones registradas.")
            return

        latest_row = plate_inspections.iloc[0]
        last_pct = int(pd.to_numeric(latest_row.get("porcentaje_cumplimiento", 0), errors="coerce") or 0)
        last_date = str(latest_row.get("fecha", ""))[:10]
        k1, k2, k3, k4 = st.columns(4)
        profile_cards = [
            ("✓", f"{last_pct}%", "Cumplimiento"),
            ("📅", last_date, "Última inspección"),
            ("⚠", len(plate_findings[plate_findings["estado"] != "Subsanado"]) if not plate_findings.empty and "estado" in plate_findings else 0, "Hallazgos abiertos"),
            ("📷", int(plate_inspections.get("evidencia_url", pd.Series(dtype=str)).fillna("").ne("").sum()), "Evidencias"),
        ]
        for col, (icon, value, label) in zip((k1, k2, k3, k4), profile_cards):
            with col:
                st.markdown(f'<div class="profile-mini-card"><span>{icon}</span><b>{value}</b><small>{label}</small></div>', unsafe_allow_html=True)

        st.markdown("### Estado actual de implementos")
        i1, i2, i3, i4 = st.columns(4)
        current_items = [
            ("cone", "Conos", int(pd.to_numeric(latest_row.get("conos_cantidad", 0), errors="coerce") or 0), "unidades"),
            ("chock", "Tacos", int(pd.to_numeric(latest_row.get("tacos_cantidad", 0), errors="coerce") or 0), "unidades"),
            ("firstaid", "Botiquín", str(latest_row.get("botiquin_estado") or "Sin dato"), ""),
            ("extinguisher", "Extintor", "Sí" if bool(latest_row.get("extintor_tiene", False)) else "No", ""),
        ]
        for col, (icon_name, label, value, suffix) in zip((i1, i2, i3, i4), current_items):
            with col:
                st.markdown(
                    f'<div class="profile-item"><div>{professional_icon(icon_name)}</div><span>{label}</span><b>{escape(str(value))} {suffix}</b></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### Historial, observaciones y evidencias")
        for _, inspection in plate_inspections.iterrows():
            inspection_id = int(inspection.get("id", 0))
            inspection_date_text = str(inspection.get("fecha", ""))[:10]
            inspection_result = str(inspection.get("resultado", "Registrada"))
            inspection_pct = int(pd.to_numeric(inspection.get("porcentaje_cumplimiento", 0), errors="coerce") or 0)
            with st.expander(
                f"Inspección #{inspection_id} · {inspection_date_text} · {inspection_result} ({inspection_pct}%)",
                expanded=False,
            ):
                st.write(f"**Inspector:** {inspection.get('inspector_nombre') or 'Sin dato'}")
                st.write(f"**Observación:** {inspection.get('observacion') or 'Sin observación'}")
                evidence_url = str(inspection.get("evidencia_url") or "").strip()
                if evidence_url:
                    st.image(evidence_url, caption=f"Evidencia · {selected_plate}", width=520)
                else:
                    st.info("Sin evidencia fotográfica en esta inspección.")

        st.markdown("### Hallazgos de la unidad")
        if plate_findings.empty:
            st.success("La unidad no tiene hallazgos registrados.")
        else:
            for _, finding in plate_findings.sort_values("created_at", ascending=False).iterrows():
                st.markdown(
                    f"""<div class="unit-finding">
                      <div><b>{escape(str(finding.get("categoria", "Hallazgo")))}</b>
                      <span>{escape(str(finding.get("estado", "Abierto")))}</span></div>
                      <p>{escape(str(finding.get("descripcion") or "Sin descripción"))}</p>
                      <small>Responsable: {escape(str(finding.get("responsable") or "Sin asignar"))} · Compromiso: {escape(str(finding.get("fecha_compromiso") or "Sin fecha"))}</small>
                    </div>""",
                    unsafe_allow_html=True,
                )
        return

    total = len(unidades)
    conformes = sum(1 for placa in unidades.get("placa", []) if latest_status.get(placa) == "Conforme")
    observadas = sum(1 for placa in unidades.get("placa", []) if latest_status.get(placa) == "Observada")
    pendientes = max(total - conformes - observadas, 0)
    c1, c2, c3, c4 = st.columns(4)
    for col, data in zip(
        (c1, c2, c3, c4),
        ((professional_icon("truck"), total, "Flota registrada", "Huachipa"), ("○", pendientes, "Pendientes", "Sin inspección"),
         ("✓", conformes, "Conformes", "Verificación completa"), ("⚠", observadas, "Observadas", "Requieren acción")),
    ):
        with col:
            metric_card(*data)

    if can_edit:
        with st.expander("➕ Registrar nueva unidad", expanded=False):
            with st.form("unit_form", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                placa = c1.text_input("Placa *").upper().strip()
                tipo = c2.selectbox("Tipo *", ["FF", "ACC", "ATG", "HINO", "PORTER", "FLI", "SMT", "TR", "MOTO", "OTRO"])
                empresa = c3.selectbox("Propiedad", ["RANSA", "Tercero/Spot"])
                marca = c1.text_input("Marca")
                modelo = c2.text_input("Modelo")
                anio = c3.number_input("Año", 1990, date.today().year + 1, date.today().year)
                agencia = c1.text_input("Agencia", value="Huachipa")
                estado = c2.selectbox("Estado", ["Activo", "Mantenimiento", "Inactivo"])
                if st.form_submit_button("Guardar unidad", type="primary"):
                    if not placa:
                        st.error("Ingresa la placa.")
                    else:
                        ok, msg = db.insert("unidades", {"placa": placa, "tipo": tipo, "empresa": empresa, "marca": marca, "modelo": modelo, "anio": int(anio), "agencia": agencia, "estado": estado, "created_by": auth.current_auth().get("user_id")})
                        (st.success if ok else st.error)(msg)
                        if ok:
                            load_all.clear(); st.rerun()
    st.markdown("### Flota operativa")
    st.caption("Selecciona una placa para consultar su estado, historial, observaciones y evidencias.")
    view = unidades.copy()
    if view.empty:
        st.warning("No hay unidades registradas en el maestro.")
        return
    for start in range(0, len(view), 4):
        cols = st.columns(4)
        for col, (_, unit) in zip(cols, view.iloc[start:start + 4].iterrows()):
            placa = str(unit.get("placa", ""))
            status = latest_status.get(placa, "Pendiente")
            css_status = {"Conforme": "ok", "Observada": "bad", "Pendiente": "pending"}[status]
            with col:
                st.markdown(
                    f'''<div class="truck-card">
                    <div class="truck-top"><span class="truck-visual">{professional_icon("truck")}</span><span class="ransa-tag">RANSA</span></div>
                    <div class="truck-plate">{placa}</div>
                    <div class="truck-meta"><span>{unit.get("tipo", "-")}</span><span>Huachipa</span></div>
                    <div class="fleet-status {css_status}"><span></span>{status}</div>
                    </div>''', unsafe_allow_html=True,
                )
                if st.button("Ver ficha completa", key=f"view_unit_{placa}", use_container_width=True):
                    st.session_state.selected_unit_plate = placa
                    st.rerun()


def inspection_page(unidades: pd.DataFrame, inspecciones: pd.DataFrame, profile: dict) -> None:
    page_header("VERIFICACIÓN OPERATIVA · PILOTO", "Nueva inspección", "Verifica los implementos obligatorios antes de la salida del camión.")
    if unidades.empty:
        st.warning("Primero registra por lo menos una unidad.")
        return
    options = {f"{r['placa']} · {r.get('tipo','')}": r for _, r in unidades.iterrows() if r.get("estado") == "Activo"}
    if not options:
        st.warning("No existen unidades activas.")
        return
    with st.container(border=True):
        c1, c2 = st.columns([1.4, 1])
        selected = c1.selectbox("Camión *", list(options))
        inspection_date = c2.date_input("Fecha de inspección", value=date.today())
        unit = options[selected]
        plate_key = str(unit["placa"]).upper().replace("-", "").replace(" ", "")
        existing_inspection = pd.DataFrame()
        if not inspecciones.empty and {"placa", "fecha"}.issubset(inspecciones.columns):
            plate_keys = (
                inspecciones["placa"].fillna("").astype(str).str.upper()
                .str.replace("-", "", regex=False).str.replace(" ", "", regex=False)
            )
            inspection_dates = pd.to_datetime(
                inspecciones["fecha"], errors="coerce"
            ).dt.date
            existing_inspection = inspecciones[
                (plate_keys == plate_key) & (inspection_dates == inspection_date)
            ]

        already_registered = not existing_inspection.empty
        if already_registered:
            existing_row = existing_inspection.sort_values(
                "created_at", ascending=False
            ).iloc[0]
            existing_id = existing_row.get("id", "")
            existing_result = existing_row.get("resultado", "Registrada")
            st.warning(
                f"⚠️ La unidad {unit['placa']} ya fue inspeccionada el "
                f"{inspection_date.strftime('%d/%m/%Y')}. "
                f"Registro #{existing_id} · {existing_result}. "
                "No se permitirá guardar una inspección duplicada."
            )

        st.markdown("#### Implementos de seguridad")
        a, b, c, d = st.columns(4)
        with a:
            st.markdown(f'<div class="inspection-icon">{professional_icon("cone")}<strong>Conos</strong></div>', unsafe_allow_html=True)
            conos_cantidad = st.number_input("Cantidad de conos", min_value=0, max_value=10, value=0, step=1)
            st.caption("Mínimo requerido: 2")
        with b:
            st.markdown(f'<div class="inspection-icon">{professional_icon("chock")}<strong>Tacos</strong></div>', unsafe_allow_html=True)
            tacos_cantidad = st.number_input("Cantidad de tacos", min_value=0, max_value=10, value=0, step=1)
            st.caption("Mínimo requerido: 2")
        with c:
            st.markdown(f'<div class="inspection-icon">{professional_icon("firstaid")}<strong>Botiquín</strong></div>', unsafe_allow_html=True)
            botiquin_estado = st.selectbox("Estado del botiquín", ["No tiene", "Incompleto", "Completo y vigente"])
            st.caption("Debe estar completo y vigente")
        with d:
            st.markdown(f'<div class="inspection-icon">{professional_icon("extinguisher")}<strong>Extintor</strong></div>', unsafe_allow_html=True)
            tiene_extintor = st.selectbox("¿Tiene extintor?", ["No", "Sí"])
            extintor_mes_nombre = st.selectbox(
                "Mes de vencimiento",
                MONTHS_ES,
                index=date.today().month - 1,
            )
            extintor_mes = MONTHS_ES.index(extintor_mes_nombre) + 1
            extintor_anio = st.number_input(
                "Año de vencimiento",
                min_value=date.today().year - 5,
                max_value=date.today().year + 10,
                value=date.today().year,
                step=1,
            )

        cumple_conos = conos_cantidad >= 2
        cumple_tacos = tacos_cantidad >= 2
        cumple_botiquin = botiquin_estado == "Completo y vigente"
        cumple_extintor = (
            tiene_extintor == "Sí"
            and (int(extintor_anio), int(extintor_mes)) >= (date.today().year, date.today().month)
        )
        criterios = [cumple_conos, cumple_tacos, cumple_botiquin, cumple_extintor]
        porcentaje = int(sum(criterios) * 25)
        resultado = "Conforme" if porcentaje == 100 else "Observada"

        st.markdown("#### Resultado de la evaluación")
        p1, p2 = st.columns([3, 1])
        with p1:
            st.progress(porcentaje / 100)
            st.caption("Cada implemento conforme representa 25% del cumplimiento.")
        with p2:
            status_class = "ok" if resultado == "Conforme" else "bad"
            st.markdown(f'<div class="score-box {status_class}"><b>{porcentaje}%</b><span>{resultado}</span></div>', unsafe_allow_html=True)

        if tiene_extintor == "Sí" and not cumple_extintor:
            st.error(
                f"El extintor está vencido: {extintor_mes_nombre} de {int(extintor_anio)}."
            )
        elif tiene_extintor == "Sí":
            st.success(
                f"Extintor vigente hasta {extintor_mes_nombre} de {int(extintor_anio)}."
            )
        observacion = st.text_area("Observación / acción inmediata")
        evidence = st.file_uploader("Evidencia fotográfica (opcional)", type=["jpg", "jpeg", "png", "webp"])
        submitted = st.button(
            "Inspección ya registrada" if already_registered else "Guardar inspección",
            type="primary",
            use_container_width=True,
            disabled=already_registered,
        )
    if submitted:
        # Segunda validación antes de subir la foto y guardar, para evitar duplicados.
        current = db.select(
            "inspecciones",
            {
                "placa": f"eq.{unit['placa']}",
                "fecha": f"eq.{inspection_date.isoformat()}",
                "limit": "1",
            },
        )
        if not current.empty:
            st.error(
                f"La unidad {unit['placa']} ya fue inspeccionada el "
                f"{inspection_date.strftime('%d/%m/%Y')}. "
                "El registro no se duplicó."
            )
            return
        ok_upload, evidence_url = db.upload_evidence(evidence, auth.current_auth().get("user_id", ""))
        if not ok_upload:
            st.error(evidence_url); return
        payload = {"unidad_id": int(unit["id"]), "placa": unit["placa"], "fecha": inspection_date.isoformat(), "inspector_id": auth.current_auth().get("user_id"), "inspector_nombre": profile.get("nombre"), "conos": cumple_conos, "tacos": cumple_tacos, "botiquin": cumple_botiquin, "extintor": cumple_extintor, "conos_cantidad": int(conos_cantidad), "tacos_cantidad": int(tacos_cantidad), "botiquin_estado": botiquin_estado, "extintor_tiene": tiene_extintor == "Sí", "extintor_anio_vencimiento": int(extintor_anio), "porcentaje_cumplimiento": porcentaje, "resultado": resultado, "observacion": observacion, "evidencia_url": evidence_url}
        if "extintor_mes_vencimiento" in inspecciones.columns:
            payload["extintor_mes_vencimiento"] = int(extintor_mes)
        ok, msg = db.insert("inspecciones", payload)
        (st.success if ok else st.error)(f"{msg} Resultado: {resultado} ({porcentaje}%)." if ok else msg)
        if ok:
            if resultado == "Observada":
                st.warning("La unidad quedó observada. Registra el hallazgo y su responsable.")
            load_all.clear()


    if not inspecciones.empty:
        st.markdown("### Corregir una inspección registrada")
        st.caption("Selecciona un registro para corregir información sin crear una inspección duplicada.")
        recent = inspecciones.sort_values(["fecha", "created_at"], ascending=False).head(50)
        edit_options = {
            f"#{int(r['id'])} · {r.get('placa', '')} · {str(r.get('fecha', ''))[:10]}": r
            for _, r in recent.iterrows()
        }
        edit_label = st.selectbox("Inspección a corregir", list(edit_options), key="edit_inspection")
        edit_row = edit_options[edit_label]
        with st.form("edit_inspection_form"):
            e1, e2, e3 = st.columns(3)
            edit_fecha_value = pd.to_datetime(edit_row.get("fecha"), errors="coerce")
            edit_fecha = e1.date_input(
                "Fecha de inspección",
                value=edit_fecha_value.date() if pd.notna(edit_fecha_value) else date.today(),
            )
            old_cones_raw = pd.to_numeric(edit_row.get("conos_cantidad", 0), errors="coerce")
            old_chocks_raw = pd.to_numeric(edit_row.get("tacos_cantidad", 0), errors="coerce")
            edit_conos = e2.number_input(
                "Cantidad de conos",
                min_value=0, max_value=10,
                value=0 if pd.isna(old_cones_raw) else int(old_cones_raw),
            )
            edit_tacos = e3.number_input(
                "Cantidad de tacos",
                min_value=0, max_value=10,
                value=0 if pd.isna(old_chocks_raw) else int(old_chocks_raw),
            )
            b1, b2, b3 = st.columns(3)
            bot_options = ["No tiene", "Incompleto", "Completo y vigente"]
            old_bot = str(edit_row.get("botiquin_estado") or "No tiene")
            edit_botiquin = b1.selectbox(
                "Estado del botiquín",
                bot_options,
                index=bot_options.index(old_bot) if old_bot in bot_options else 0,
            )
            edit_tiene_ext = b2.selectbox(
                "¿Tiene extintor?",
                ["No", "Sí"],
                index=1 if bool(edit_row.get("extintor_tiene", False)) else 0,
            )
            old_month_raw = pd.to_numeric(
                edit_row.get("extintor_mes_vencimiento", date.today().month),
                errors="coerce",
            )
            old_month = date.today().month if pd.isna(old_month_raw) else int(old_month_raw)
            old_month = min(max(old_month, 1), 12)
            edit_mes_nombre = b3.selectbox("Mes de vencimiento", MONTHS_ES, index=old_month - 1)
            edit_mes = MONTHS_ES.index(edit_mes_nombre) + 1
            d1, d2 = st.columns([1, 2])
            old_year_raw = pd.to_numeric(
                edit_row.get("extintor_anio_vencimiento", date.today().year),
                errors="coerce",
            )
            old_year = date.today().year if pd.isna(old_year_raw) else int(old_year_raw)
            edit_anio = d1.number_input(
                "Año de vencimiento",
                min_value=date.today().year - 5,
                max_value=date.today().year + 10,
                value=old_year,
            )
            edit_observacion = d2.text_area(
                "Observación / acción inmediata",
                value=str(edit_row.get("observacion") or ""),
            )
            save_edit = st.form_submit_button("Guardar corrección", type="primary", use_container_width=True)

        if save_edit:
            record_id = int(edit_row["id"])
            placa_edit = str(edit_row.get("placa", ""))
            other_dates = pd.to_datetime(inspecciones.get("fecha"), errors="coerce").dt.date
            duplicate = inspecciones[
                (inspecciones["placa"].astype(str).str.upper() == placa_edit.upper())
                & (other_dates == edit_fecha)
                & (inspecciones["id"].astype(int) != record_id)
            ]
            if not duplicate.empty:
                st.error(f"{placa_edit} ya tiene otra inspección registrada el {edit_fecha.strftime('%d/%m/%Y')}.")
            else:
                edit_conos_ok = int(edit_conos) >= 2
                edit_tacos_ok = int(edit_tacos) >= 2
                edit_bot_ok = edit_botiquin == "Completo y vigente"
                edit_ext_ok = (
                    edit_tiene_ext == "Sí"
                    and (int(edit_anio), int(edit_mes)) >= (date.today().year, date.today().month)
                )
                edit_pct = int(sum([edit_conos_ok, edit_tacos_ok, edit_bot_ok, edit_ext_ok]) * 25)
                edit_data = {
                    "fecha": edit_fecha.isoformat(),
                    "conos_cantidad": int(edit_conos),
                    "tacos_cantidad": int(edit_tacos),
                    "conos": edit_conos_ok,
                    "tacos": edit_tacos_ok,
                    "botiquin_estado": edit_botiquin,
                    "botiquin": edit_bot_ok,
                    "extintor_tiene": edit_tiene_ext == "Sí",
                    "extintor_anio_vencimiento": int(edit_anio),
                    "extintor": edit_ext_ok,
                    "porcentaje_cumplimiento": edit_pct,
                    "resultado": "Conforme" if edit_pct == 100 else "Observada",
                    "observacion": edit_observacion,
                }
                if "extintor_mes_vencimiento" in inspecciones.columns:
                    edit_data["extintor_mes_vencimiento"] = int(edit_mes)
                ok, msg = db.update("inspecciones", record_id, edit_data)
                (st.success if ok else st.error)(msg)
                if ok:
                    load_all.clear()
                    st.rerun()


def findings_page(hallazgos: pd.DataFrame, inspecciones: pd.DataFrame, can_edit: bool) -> None:
    page_header("CENTRO DE CONTROL PREVENTIVO", "Hallazgos", "Prioriza riesgos, asigna responsables y controla cada acción hasta su cierre.")

    findings = hallazgos.copy()
    if not findings.empty:
        findings["fecha_compromiso_dt"] = pd.to_datetime(findings.get("fecha_compromiso"), errors="coerce")
    abiertos = findings[findings.get("estado", pd.Series(dtype=str)) != "Subsanado"] if not findings.empty else pd.DataFrame()
    total_abiertos = len(abiertos)
    alta_critica = int(abiertos.get("criticidad", pd.Series(dtype=str)).isin(["Alta", "Crítica"]).sum()) if not abiertos.empty else 0
    vencidos = int((abiertos.get("fecha_compromiso_dt", pd.Series(dtype="datetime64[ns]")) < pd.Timestamp.today().normalize()).sum()) if not abiertos.empty else 0
    subsanados = int((findings.get("estado", pd.Series(dtype=str)) == "Subsanado").sum()) if not findings.empty else 0

    k1, k2, k3, k4 = st.columns(4)
    summary = [
        ("⚑", total_abiertos, "Hallazgos abiertos", "Requieren seguimiento"),
        ("!", alta_critica, "Alta prioridad", "Alta o crítica"),
        ("◷", vencidos, "Fuera de plazo", "Acción inmediata"),
        ("✓", subsanados, "Subsanados", "Cierre verificado"),
    ]
    for col, card in zip((k1, k2, k3, k4), summary):
        with col:
            metric_card(*card)

    if can_edit:
        observed = inspecciones[inspecciones.get("resultado", pd.Series(dtype=str)) == "Observada"] if not inspecciones.empty else pd.DataFrame()
        with st.expander("＋ Registrar nuevo hallazgo", expanded=hallazgos.empty):
            with st.form("finding_form", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                ref_options = ["Sin inspección vinculada"] + ([f"#{int(r['id'])} · {r['placa']} · {r['fecha']}" for _, r in observed.iterrows()] if not observed.empty else [])
                ref = c1.selectbox("Inspección relacionada", ref_options)
                placa = c2.text_input("Placa *").upper()
                categoria = c3.selectbox("Categoría", ["Implementos", "Extintor vencido", "Extintor operativo", "Botiquín", "Conos", "Tacos", "Seguridad", "Otro"])
                descripcion = st.text_area("Descripción concreta del hallazgo *", height=110, placeholder="Describe qué se encontró, el riesgo y la acción inmediata requerida.")
                c4, c5, c6 = st.columns(3)
                criticidad = c4.selectbox("Criticidad", ["Baja", "Media", "Alta", "Crítica"])
                responsable = c5.text_input("Responsable *", placeholder="Nombre del responsable")
                compromiso = c6.date_input("Fecha compromiso", date.today() + timedelta(days=1))
                if st.form_submit_button("Guardar hallazgo", type="primary"):
                    inspection_id = None if ref.startswith("Sin") else int(ref.split("#")[1].split(" ")[0])
                    if not placa or not descripcion or not responsable:
                        st.error("Completa placa, descripción y responsable.")
                    else:
                        ok, msg = db.insert("hallazgos", {"inspeccion_id": inspection_id, "placa": placa, "fecha": date.today().isoformat(), "categoria": categoria, "descripcion": descripcion, "criticidad": criticidad, "responsable": responsable, "fecha_compromiso": compromiso.isoformat(), "estado": "Abierto", "created_by": auth.current_auth().get("user_id")})
                        (st.success if ok else st.error)(msg)
                        if ok: load_all.clear(); st.rerun()
    if hallazgos.empty:
        st.markdown('''<div class="findings-empty"><div class="findings-empty-icon">✓</div>
        <h3>Flota sin hallazgos registrados</h3><p>Cuando una inspección resulte observada, registra aquí el riesgo, responsable y fecha compromiso.</p>
        <div class="empty-flow"><span>1 · Detectar</span><span>2 · Asignar</span><span>3 · Subsanar</span></div></div>''', unsafe_allow_html=True)
        return

    st.markdown("### Seguimiento activo")
    f1, f2 = st.columns(2)
    status = f1.multiselect("Estado", ["Abierto", "En proceso", "Subsanado"], default=["Abierto", "En proceso"])
    criticality = f2.multiselect("Criticidad", ["Baja", "Media", "Alta", "Crítica"])
    view = hallazgos.copy()
    if status: view = view[view["estado"].isin(status)]
    if criticality: view = view[view["criticidad"].isin(criticality)]

    if view.empty:
        st.info("No hay hallazgos que coincidan con los filtros seleccionados.")
    else:
        for _, row in view.head(20).iterrows():
            crit = str(row.get("criticidad", "Baja"))
            crit_class = {"Baja": "low", "Media": "medium", "Alta": "high", "Crítica": "critical"}.get(crit, "low")
            st.markdown(f'''<div class="finding-card {crit_class}">
              <div class="finding-head"><div><span class="finding-id">#{int(row.get("id", 0))}</span><b>{escape(str(row.get("placa", "")))}</b></div>
              <span class="criticality-pill">{escape(crit)}</span></div>
              <div class="finding-category">{escape(str(row.get("categoria", "")))}</div>
              <p>{escape(str(row.get("descripcion", "")))}</p>
              <div class="finding-footer"><span>Responsable: <b>{escape(str(row.get("responsable", "Sin asignar")))}</b></span>
              <span>Compromiso: <b>{escape(str(row.get("fecha_compromiso", "")))}</b></span>
              <span class="state-pill">{escape(str(row.get("estado", "Abierto")))}</span></div>
            </div>''', unsafe_allow_html=True)
    if can_edit and not view.empty:
        st.markdown("#### Corregir o actualizar un hallazgo")
        edit_ids = view["id"].tolist()
        record_id = st.selectbox(
            "Hallazgo a modificar",
            edit_ids,
            format_func=lambda x: f"#{x} · {view.loc[view['id'] == x, 'placa'].iloc[0]}",
        )
        selected_finding = view[view["id"] == record_id].iloc[0]
        with st.form("edit_finding_form"):
            h1, h2, h3 = st.columns(3)
            edit_placa = h1.text_input("Placa", value=str(selected_finding.get("placa") or "")).upper().strip()
            category_options = ["Implementos", "Extintor vencido", "Extintor operativo", "Botiquín", "Conos", "Tacos", "Seguridad", "Otro"]
            old_category = str(selected_finding.get("categoria") or "Otro")
            edit_category = h2.selectbox(
                "Categoría",
                category_options,
                index=category_options.index(old_category) if old_category in category_options else len(category_options) - 1,
            )
            criticality_options = ["Baja", "Media", "Alta", "Crítica"]
            old_criticality = str(selected_finding.get("criticidad") or "Baja")
            edit_criticality = h3.selectbox(
                "Criticidad",
                criticality_options,
                index=criticality_options.index(old_criticality) if old_criticality in criticality_options else 0,
            )
            edit_description = st.text_area(
                "Descripción del hallazgo",
                value=str(selected_finding.get("descripcion") or ""),
                height=100,
            )
            j1, j2, j3 = st.columns(3)
            edit_responsible = j1.text_input(
                "Responsable",
                value=str(selected_finding.get("responsable") or ""),
            )
            old_commitment = pd.to_datetime(selected_finding.get("fecha_compromiso"), errors="coerce")
            edit_commitment = j2.date_input(
                "Fecha compromiso",
                value=old_commitment.date() if pd.notna(old_commitment) else date.today(),
            )
            status_options = ["Abierto", "En proceso", "Subsanado"]
            old_status = str(selected_finding.get("estado") or "Abierto")
            edit_status = j3.selectbox(
                "Estado",
                status_options,
                index=status_options.index(old_status) if old_status in status_options else 0,
            )
            update_finding = st.form_submit_button(
                "Guardar cambios del hallazgo",
                type="primary",
                use_container_width=True,
            )
        if update_finding:
            if not edit_placa or not edit_description or not edit_responsible:
                st.error("Completa placa, descripción y responsable.")
            else:
                final_status = "Subsanado" if edit_category == "Extintor operativo" else edit_status
                final_description = edit_description
                if edit_category == "Extintor operativo" and "operativo" not in edit_description.lower():
                    final_description = f"Extintor operativo y vigente. {edit_description}".strip()
                ok, msg = db.update(
                    "hallazgos",
                    record_id,
                    {
                        "placa": edit_placa,
                        "categoria": edit_category,
                        "descripcion": final_description,
                        "criticidad": edit_criticality,
                        "responsable": edit_responsible,
                        "fecha_compromiso": edit_commitment.isoformat(),
                        "estado": final_status,
                    },
                )
                if ok and edit_category == "Extintor operativo":
                    st.success("Hallazgo actualizado: extintor operativo y estado Subsanado.")
                else:
                    (st.success if ok else st.error)(msg)
                if ok:
                    load_all.clear()
                    st.rerun()


def evidence_page(inspecciones: pd.DataFrame, hallazgos: pd.DataFrame) -> None:
    page_header("TRAZABILIDAD VISUAL", "Evidencias", "Consulta las fotografías asociadas a inspecciones y hallazgos.")
    rows = []
    seen = set()
    for source, frame in [("Inspección", inspecciones), ("Hallazgo", hallazgos)]:
        if not frame.empty and "evidencia_url" in frame:
            for _, row in frame[frame["evidencia_url"].fillna("") != ""].iterrows():
                plate_key = str(row.get("placa", "")).upper().replace("-", "").replace(" ", "")
                date_key = str(row.get("fecha", ""))[:10]
                evidence_key = (source, plate_key, date_key)
                if evidence_key in seen:
                    continue
                seen.add(evidence_key)
                rows.append((source, row.get("placa", ""), row.get("fecha", ""), row.get("evidencia_url", "")))
    if not rows:
        st.info("Aún no existen evidencias fotográficas."); return
    for start in range(0, len(rows), 3):
        cols = st.columns(3)
        for col, item in zip(cols, rows[start:start+3]):
            with col:
                st.image(item[3], use_container_width=True)
                st.caption(f"{item[0]} · {item[1]} · {item[2]}")


def reports_page(unidades: pd.DataFrame, inspecciones: pd.DataFrame, hallazgos: pd.DataFrame) -> None:
    page_header("ANÁLISIS Y DECISIÓN", "Reportes", "Filtra el periodo y analiza cumplimiento, observaciones y tendencias.")
    ins = normalize_dates(inspecciones)
    c1, c2 = st.columns(2)
    start = c1.date_input("Desde", date.today() - timedelta(days=30))
    end = c2.date_input("Hasta", date.today())
    filtered = ins[(ins["fecha"].dt.date >= start) & (ins["fecha"].dt.date <= end)] if not ins.empty else ins
    if filtered.empty:
        st.info("No existen inspecciones en el periodo seleccionado."); return
    a, b = st.columns(2)
    with a:
        counts = filtered["resultado"].value_counts().rename_axis("Resultado").reset_index(name="Cantidad")
        fig = px.bar(counts, x="Resultado", y="Cantidad", color="Resultado", text="Cantidad", color_discrete_map={"Conforme":"#00a86b", "Observada":"#f59e0b"})
        fig.update_layout(title="Resultados de inspección", showlegend=False, height=350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False, "staticPlot":True})
    with b:
        daily = filtered.groupby([filtered["fecha"].dt.date, "resultado"]).size().reset_index(name="Cantidad")
        daily.columns = ["Fecha", "Resultado", "Cantidad"]
        fig = px.line(daily, x="Fecha", y="Cantidad", color="Resultado", markers=True, color_discrete_map={"Conforme":"#00a86b", "Observada":"#f59e0b"})
        fig.update_layout(title="Evolución diaria", height=350)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False, "staticPlot":True})
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    st.download_button("⬇ Descargar reporte filtrado", excel_bytes({"Inspecciones": filtered, "Hallazgos": hallazgos, "Unidades": unidades}), "reporte_filtrado_ssoma.xlsx")


def users_page() -> None:
    page_header("CONTROL DE ACCESO", "Usuarios y privilegios", "Crea cuentas y asigna el nivel de acceso correspondiente.")
    roles = {"Administrador": "Acceso total y creación de usuarios.", "Inspector": "Registra unidades, inspecciones y hallazgos.", "Consulta": "Solo visualiza dashboards y reportes."}
    st.info(" · ".join([f"**{k}:** {v}" for k, v in roles.items()]))
    with st.form("new_user", clear_on_submit=True):
        c1, c2 = st.columns(2)
        nombre = c1.text_input("Nombre completo *")
        username = c2.text_input("Usuario *", placeholder="gllajae").strip().lower()
        password = c1.text_input("Contraseña temporal *", type="password", help="Mínimo 8 caracteres")
        role = c2.selectbox("Rol", list(roles))
        contact_email = st.text_input("Correo de contacto (opcional)", placeholder="persona@gmail.com")
        if st.form_submit_button("Crear usuario", type="primary"):
            valid_username = username and username.replace("_", "").replace("-", "").isalnum()
            if not nombre or not valid_username or len(password) < 8:
                st.error("Completa nombre y usuario. La contraseña debe tener mínimo 8 caracteres.")
            else:
                internal_email = f"{username}@kaironix.local"
                ok, msg, user_id = auth.create_auth_user(internal_email, password, nombre)
                if ok:
                    ok2, msg2 = db.insert("profiles", {"id": user_id, "nombre": nombre, "username": username, "email": internal_email, "correo_contacto": contact_email.strip().lower() or None, "rol": role, "activo": True}, admin=True)
                    (st.success if ok2 else st.error)(msg2 if not ok2 else f"{msg} Rol asignado: {role}.")
                else: st.error(msg)
    profiles = db.select("profiles", {"order": "created_at.desc"}, admin=True)
    if not profiles.empty:
        st.dataframe(profiles[[c for c in ["nombre", "username", "correo_contacto", "rol", "activo", "created_at"] if c in profiles]], use_container_width=True, hide_index=True)


if not auth.current_auth():
    login_screen()
    st.stop()

profile = load_session_profile()
if not profile or not profile.get("activo", False):
    st.error("Tu cuenta no tiene un perfil activo. Solicita acceso al administrador.")
    if st.button("Cerrar sesión"):
        auth.sign_out(); st.rerun()
    st.stop()

page = sidebar(profile)
role = profile.get("rol", "Consulta")
can_edit = role in ("Administrador", "Inspector")
unidades, inspecciones, hallazgos = load_all()

if page == "Inicio": dashboard(unidades, inspecciones, hallazgos)
elif page == "Unidades": units_page(unidades, inspecciones, hallazgos, can_edit, role == "Administrador")
elif page == "Nueva inspección":
    if can_edit: inspection_page(unidades, inspecciones, profile)
    else: st.warning("Tu perfil es de consulta y no permite registrar inspecciones.")
elif page == "Hallazgos": findings_page(hallazgos, inspecciones, can_edit)
elif page == "Evidencias": evidence_page(inspecciones, hallazgos)
elif page == "Reportes": reports_page(unidades, inspecciones, hallazgos)
elif page == "Usuarios" and role == "Administrador": users_page()
