from __future__ import annotations

from datetime import date, timedelta
from io import BytesIO

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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


def professional_icon(name: str) -> str:
    icons = {
        "truck": '''<svg class="pro-icon truck-svg" viewBox="0 0 72 48" aria-label="Camión RANSA">
          <rect x="4" y="11" width="38" height="24" rx="4" fill="#ffffff" stroke="#007953" stroke-width="2"/>
          <rect x="42" y="19" width="19" height="16" rx="3" fill="#00a86b"/>
          <path d="M47 20h8l5 7H47z" fill="#dff8ed"/><rect x="10" y="18" width="26" height="9" rx="2" fill="#007953"/>
          <text x="23" y="25" text-anchor="middle" font-size="7" font-weight="900" fill="white">RANSA</text>
          <circle cx="17" cy="38" r="6" fill="#10243e"/><circle cx="17" cy="38" r="2.5" fill="#d7e1de"/>
          <circle cx="52" cy="38" r="6" fill="#10243e"/><circle cx="52" cy="38" r="2.5" fill="#d7e1de"/>
        </svg>''',
        "cone": '''<svg class="pro-icon" viewBox="0 0 48 48" aria-label="Conos">
          <path d="M18 5h12l7 31H11z" fill="#ff7a00"/><path d="M15 19h18l2 8H13z" fill="#fff"/>
          <rect x="6" y="36" width="36" height="7" rx="3" fill="#e35300"/>
        </svg>''',
        "chock": '''<svg class="pro-icon" viewBox="0 0 48 48" aria-label="Tacos de rueda">
          <path d="M7 37V25c12 0 19-7 24-17l10 29z" fill="#182235"/>
          <path d="M11 30l5-2 3 9h-6zm10-6 5-4 6 17h-7z" fill="#f5b400"/>
          <rect x="5" y="37" width="38" height="5" rx="2" fill="#0a1322"/>
        </svg>''',
        "firstaid": '''<svg class="pro-icon" viewBox="0 0 48 48" aria-label="Botiquín">
          <rect x="5" y="13" width="38" height="29" rx="6" fill="#e43d45"/>
          <path d="M17 13V9c0-2 2-4 4-4h6c2 0 4 2 4 4v4" fill="none" stroke="#a91f2a" stroke-width="4"/>
          <rect x="20" y="20" width="8" height="16" rx="1" fill="#fff"/><rect x="16" y="24" width="16" height="8" rx="1" fill="#fff"/>
        </svg>''',
        "extinguisher": '''<svg class="pro-icon" viewBox="0 0 48 48" aria-label="Extintor">
          <path d="M20 8h12l4 7v25c0 3-2 5-5 5H17c-3 0-5-2-5-5V20c0-6 3-10 8-12z" fill="#e33b32"/>
          <rect x="18" y="4" width="14" height="6" rx="2" fill="#26354a"/><path d="M31 7h9v5h-5" fill="none" stroke="#26354a" stroke-width="3"/>
          <path d="M36 11c7 4 5 13 3 18" fill="none" stroke="#26354a" stroke-width="3" stroke-linecap="round"/>
          <rect x="17" y="22" width="14" height="9" rx="2" fill="#fff"/><path d="M20 26h8" stroke="#e33b32" stroke-width="2"/>
        </svg>''',
    }
    return icons[name]


st.set_page_config(page_title="Kaironix SSOMA 360", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    left, center, right = st.columns([1.2, 1, 1.2])
    with center:
        st.markdown(
            """<div style="text-align:center;margin-bottom:20px">
            <div style="font-size:3rem">🛡️</div>
            <h1 style="margin:0">Kaironix <span style="color:#00a86b">SSOMA 360</span></h1>
            <p style="color:#607286">Control preventivo de flota</p></div>""",
            unsafe_allow_html=True,
        )
        if not auth.configured():
            st.error("El proyecto todavía no tiene configuradas las credenciales de Supabase.")
        with st.form("login_form"):
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
        st.caption("Acceso exclusivo para usuarios autorizados.")


def load_session_profile() -> dict:
    current = auth.current_auth()
    if not current:
        return {}
    if "profile" not in st.session_state:
        st.session_state.profile = db.get_profile(current.get("user_id", ""))
    return st.session_state.get("profile", {})


def sidebar(profile: dict) -> str:
    role = profile.get("rol", "Consulta")
    st.sidebar.markdown('<div class="brand">🛡️ Kaironix<br><span>SSOMA 360</span></div>', unsafe_allow_html=True)
    st.sidebar.caption("Piloto · CBC Huachipa")
    st.sidebar.markdown("---")
    pages = ["Inicio", "Unidades", "Nueva inspección", "Hallazgos", "Evidencias", "Reportes"]
    if role == "Administrador":
        pages.append("Usuarios")
    selected = st.sidebar.radio("Navegación", pages, label_visibility="collapsed")
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
    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c1:
        st.subheader("Cumplimiento general")
        values = [conformes, observadas, pending]
        fig = go.Figure(go.Pie(values=values if sum(values) else [1], labels=["Conformes", "Observadas", "Pendientes"], hole=.72, marker_colors=["#00a86b", "#f59e0b", "#d7e1de"], textinfo="none"))
        pct = round((conformes / total * 100), 1) if total else 0
        fig.add_annotation(text=f"<b>{pct}%</b><br><span style='font-size:12px'>cumplimiento</span>", showarrow=False, font_size=24)
        fig.update_layout(height=330, margin=dict(l=5, r=5, t=5, b=5), legend=dict(orientation="h", y=-.05))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "staticPlot": True})
    with c2:
        st.subheader("Estado de implementos")
        items = [("cone", "Conos", "conos"), ("chock", "Tacos", "tacos"), ("firstaid", "Botiquín", "botiquin"), ("extinguisher", "Extintor", "extintor")]
        for icon_name, label, field in items:
            count = int(latest[field].fillna(False).astype(bool).sum()) if not latest.empty and field in latest else 0
            st.markdown(f'<div class="equipment-row">{professional_icon(icon_name)}<strong>{label}</strong><span>{count}/{inspected}</span></div>', unsafe_allow_html=True)
            st.progress(count / inspected if inspected else 0)
        st.info("Las barras se actualizan con la última inspección de cada unidad.")
    with c3:
        st.subheader("Alertas prioritarias")
        open_h = hallazgos[hallazgos["estado"] != "Subsanado"] if not hallazgos.empty and "estado" in hallazgos else pd.DataFrame()
        if open_h.empty:
            st.markdown("<div style='text-align:center;padding:70px 5px'>🛡️<h3>Sin alertas registradas</h3><p>Las observaciones aparecerán aquí.</p></div>", unsafe_allow_html=True)
        else:
            for _, row in open_h.head(5).iterrows():
                st.warning(f"**{row.get('placa','')} · {row.get('criticidad','')}**\n\n{row.get('descripcion','')}")
    st.download_button("⬇ Exportar información a Excel", excel_bytes({"Unidades": unidades, "Inspecciones": inspecciones, "Hallazgos": hallazgos}), "reporte_ssoma_360.xlsx", use_container_width=False)


def units_page(unidades: pd.DataFrame, inspecciones: pd.DataFrame, can_edit: bool, is_admin: bool) -> None:
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
    search = st.text_input("🔎 Buscar por placa o tipo")
    view = unidades.copy()
    if search and not view.empty:
        mask = view.astype(str).apply(lambda row: row.str.contains(search, case=False, na=False).any(), axis=1)
        view = view[mask]
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


def inspection_page(unidades: pd.DataFrame, profile: dict) -> None:
    page_header("VERIFICACIÓN OPERATIVA", "Nueva inspección", "Registra la evaluación preventiva antes de la salida de la unidad.")
    if unidades.empty:
        st.warning("Primero registra por lo menos una unidad.")
        return
    options = {f"{r['placa']} · {r.get('tipo','')}": r for _, r in unidades.iterrows() if r.get("estado") == "Activo"}
    if not options:
        st.warning("No existen unidades activas.")
        return
    with st.form("inspection_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        selected = c1.selectbox("Unidad *", list(options))
        inspection_date = c2.date_input("Fecha", value=date.today())
        km = c3.number_input("Kilometraje", min_value=0, step=1)
        st.markdown("#### Lista de verificación")
        a, b, c, d = st.columns(4)
        conos = a.checkbox("Conos")
        tacos = a.checkbox("Tacos")
        botiquin = b.checkbox("Botiquín")
        extintor = b.checkbox("Extintor")
        luces = c.checkbox("Luces")
        neumaticos = c.checkbox("Neumáticos")
        cinturones = d.checkbox("Cinturones")
        documentos = d.checkbox("Documentos")
        observacion = st.text_area("Observación / acción inmediata")
        evidence = st.file_uploader("Evidencia fotográfica (opcional)", type=["jpg", "jpeg", "png", "webp"])
        submitted = st.form_submit_button("Guardar inspección", type="primary", use_container_width=True)
    if submitted:
        checks = [conos, tacos, botiquin, extintor, luces, neumaticos, cinturones, documentos]
        resultado = "Conforme" if all(checks) else "Observada"
        ok_upload, evidence_url = db.upload_evidence(evidence, auth.current_auth().get("user_id", ""))
        if not ok_upload:
            st.error(evidence_url); return
        unit = options[selected]
        payload = {"unidad_id": int(unit["id"]), "placa": unit["placa"], "fecha": inspection_date.isoformat(), "inspector_id": auth.current_auth().get("user_id"), "inspector_nombre": profile.get("nombre"), "kilometraje": km, "conos": conos, "tacos": tacos, "botiquin": botiquin, "extintor": extintor, "luces": luces, "neumaticos": neumaticos, "cinturones": cinturones, "documentos": documentos, "resultado": resultado, "observacion": observacion, "evidencia_url": evidence_url}
        ok, msg = db.insert("inspecciones", payload)
        (st.success if ok else st.error)(f"{msg} Resultado: {resultado}" if ok else msg)
        if ok:
            if resultado == "Observada":
                st.warning("La unidad quedó observada. Registra el hallazgo y su responsable.")
            load_all.clear()


def findings_page(hallazgos: pd.DataFrame, inspecciones: pd.DataFrame, can_edit: bool) -> None:
    page_header("GESTIÓN PREVENTIVA", "Hallazgos", "Asigna responsables y controla la subsanación de observaciones.")
    if can_edit:
        observed = inspecciones[inspecciones.get("resultado", pd.Series(dtype=str)) == "Observada"] if not inspecciones.empty else pd.DataFrame()
        with st.expander("➕ Registrar hallazgo", expanded=hallazgos.empty):
            with st.form("finding_form", clear_on_submit=True):
                c1, c2, c3 = st.columns(3)
                ref_options = ["Sin inspección vinculada"] + ([f"#{int(r['id'])} · {r['placa']} · {r['fecha']}" for _, r in observed.iterrows()] if not observed.empty else [])
                ref = c1.selectbox("Inspección relacionada", ref_options)
                placa = c2.text_input("Placa *").upper()
                categoria = c3.selectbox("Categoría", ["Implementos", "Documentación", "Mecánico", "Neumáticos", "Seguridad", "Limpieza", "Otro"])
                descripcion = st.text_area("Descripción del hallazgo *")
                c4, c5, c6 = st.columns(3)
                criticidad = c4.selectbox("Criticidad", ["Baja", "Media", "Alta", "Crítica"])
                responsable = c5.text_input("Responsable")
                compromiso = c6.date_input("Fecha compromiso", date.today() + timedelta(days=1))
                if st.form_submit_button("Guardar hallazgo", type="primary"):
                    inspection_id = None if ref.startswith("Sin") else int(ref.split("#")[1].split(" ")[0])
                    if not placa or not descripcion:
                        st.error("Completa la placa y la descripción.")
                    else:
                        ok, msg = db.insert("hallazgos", {"inspeccion_id": inspection_id, "placa": placa, "fecha": date.today().isoformat(), "categoria": categoria, "descripcion": descripcion, "criticidad": criticidad, "responsable": responsable, "fecha_compromiso": compromiso.isoformat(), "estado": "Abierto", "created_by": auth.current_auth().get("user_id")})
                        (st.success if ok else st.error)(msg)
                        if ok: load_all.clear(); st.rerun()
    if hallazgos.empty:
        st.info("No hay hallazgos registrados."); return
    f1, f2 = st.columns(2)
    status = f1.multiselect("Estado", ["Abierto", "En proceso", "Subsanado"], default=["Abierto", "En proceso"])
    criticality = f2.multiselect("Criticidad", ["Baja", "Media", "Alta", "Crítica"])
    view = hallazgos.copy()
    if status: view = view[view["estado"].isin(status)]
    if criticality: view = view[view["criticidad"].isin(criticality)]
    st.dataframe(view[[c for c in ["id", "fecha", "placa", "categoria", "descripcion", "criticidad", "responsable", "fecha_compromiso", "estado"] if c in view]], use_container_width=True, hide_index=True)
    if can_edit and not view.empty:
        st.markdown("#### Actualizar estado")
        c1, c2, c3 = st.columns([1, 1, 1])
        record_id = c1.selectbox("Hallazgo", view["id"].tolist(), format_func=lambda x: f"#{x}")
        new_status = c2.selectbox("Nuevo estado", ["Abierto", "En proceso", "Subsanado"])
        if c3.button("Actualizar", use_container_width=True):
            ok, msg = db.update("hallazgos", record_id, {"estado": new_status})
            (st.success if ok else st.error)(msg)
            if ok: load_all.clear(); st.rerun()


def evidence_page(inspecciones: pd.DataFrame, hallazgos: pd.DataFrame) -> None:
    page_header("TRAZABILIDAD VISUAL", "Evidencias", "Consulta las fotografías asociadas a inspecciones y hallazgos.")
    rows = []
    for source, frame in [("Inspección", inspecciones), ("Hallazgo", hallazgos)]:
        if not frame.empty and "evidencia_url" in frame:
            for _, row in frame[frame["evidencia_url"].fillna("") != ""].iterrows():
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
elif page == "Unidades": units_page(unidades, inspecciones, can_edit, role == "Administrador")
elif page == "Nueva inspección":
    if can_edit: inspection_page(unidades, profile)
    else: st.warning("Tu perfil es de consulta y no permite registrar inspecciones.")
elif page == "Hallazgos": findings_page(hallazgos, inspecciones, can_edit)
elif page == "Evidencias": evidence_page(inspecciones, hallazgos)
elif page == "Reportes": reports_page(unidades, inspecciones, hallazgos)
elif page == "Usuarios" and role == "Administrador": users_page()
