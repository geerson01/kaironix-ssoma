from __future__ import annotations

import requests
import streamlit as st


def _secret(name: str) -> str:
    try:
        return str(st.secrets[name]).strip()
    except Exception:
        return ""


def configured() -> bool:
    return bool(_secret("SUPABASE_URL") and _secret("SUPABASE_ANON_KEY"))


def sign_in(email: str, password: str) -> tuple[bool, str]:
    url = _secret("SUPABASE_URL")
    key = _secret("SUPABASE_ANON_KEY")
    if not url or not key:
        return False, "Falta configurar Supabase en los Secrets de Streamlit."
    try:
        response = requests.post(
            f"{url}/auth/v1/token?grant_type=password",
            headers={"apikey": key, "Content-Type": "application/json"},
            json={"email": email.strip().lower(), "password": password},
            timeout=20,
        )
        if response.status_code >= 400:
            return False, "Correo o contraseña incorrectos."
        data = response.json()
        user = data.get("user", {})
        st.session_state.auth = {
            "access_token": data.get("access_token", ""),
            "refresh_token": data.get("refresh_token", ""),
            "user_id": user.get("id", ""),
            "email": user.get("email", email),
        }
        return True, "Ingreso correcto."
    except requests.RequestException:
        return False, "No se pudo conectar con el servidor de acceso."


def sign_out() -> None:
    st.session_state.pop("auth", None)
    st.session_state.pop("profile", None)


def current_auth() -> dict:
    return st.session_state.get("auth", {})


def create_auth_user(email: str, password: str, nombre: str) -> tuple[bool, str, str]:
    url = _secret("SUPABASE_URL")
    service_key = _secret("SUPABASE_SERVICE_ROLE_KEY")
    if not service_key:
        return False, "Falta SUPABASE_SERVICE_ROLE_KEY en los Secrets.", ""
    try:
        response = requests.post(
            f"{url}/auth/v1/admin/users",
            headers={
                "apikey": service_key,
                "Authorization": f"Bearer {service_key}",
                "Content-Type": "application/json",
            },
            json={
                "email": email.strip().lower(),
                "password": password,
                "email_confirm": True,
                "user_metadata": {"nombre": nombre},
            },
            timeout=20,
        )
        if response.status_code >= 400:
            detail = response.json().get("msg") or response.json().get("message") or "No se pudo crear."
            return False, str(detail), ""
        user_id = response.json().get("id", "")
        return True, "Usuario creado correctamente.", user_id
    except requests.RequestException:
        return False, "No se pudo conectar con Supabase Auth.", ""

