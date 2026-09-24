from __future__ import annotations

import base64
import json
import time

import requests
import streamlit as st


def _secret(name: str) -> str:
    try:
        return str(st.secrets[name]).strip()
    except Exception:
        return ""


def configured() -> bool:
    return bool(_secret("SUPABASE_URL") and _secret("SUPABASE_ANON_KEY"))


def _resolve_login_email(identifier: str) -> str:
    """Resuelve un usuario visible a su correo técnico de Supabase Auth."""
    identifier = identifier.strip().lower()
    if "@" in identifier:
        return identifier
    url = _secret("SUPABASE_URL")
    secret_key = _secret("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not secret_key:
        return ""
    try:
        response = requests.get(
            f"{url}/rest/v1/profiles",
            headers={"apikey": secret_key},
            params={"select": "email", "username": f"eq.{identifier}", "limit": "1"},
            timeout=20,
        )
        response.raise_for_status()
        rows = response.json()
        return str(rows[0].get("email", "")) if rows else ""
    except requests.RequestException:
        return ""


def sign_in(identifier: str, password: str) -> tuple[bool, str]:
    url = _secret("SUPABASE_URL")
    key = _secret("SUPABASE_ANON_KEY")
    if not url or not key:
        return False, "Falta configurar Supabase en los Secrets de Streamlit."
    email = _resolve_login_email(identifier)
    if not email:
        return False, "Usuario o contraseña incorrectos."
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
            "expires_at": time.time() + int(data.get("expires_in", 3600)),
            "user_id": user.get("id", ""),
            "email": user.get("email", email),
        }
        return True, "Ingreso correcto."
    except requests.RequestException:
        return False, "No se pudo conectar con el servidor de acceso."


def sign_out() -> None:
    st.session_state.pop("auth", None)
    st.session_state.pop("profile", None)


def _token_expiry(token: str) -> int:
    try:
        segment = token.split(".")[1]
        payload = json.loads(base64.urlsafe_b64decode(segment + "=" * (-len(segment) % 4)))
        return int(payload.get("exp", 0))
    except (IndexError, ValueError, TypeError):
        return 0


def refresh_session(force: bool = False) -> bool:
    session = st.session_state.get("auth", {})
    if not session:
        return False
    expiry = session.get("expires_at") or _token_expiry(session.get("access_token", ""))
    if not force and expiry and time.time() < float(expiry) - 120:
        return True
    refresh_token = session.get("refresh_token")
    if not refresh_token:
        return False
    try:
        response = requests.post(
            f"{_secret('SUPABASE_URL')}/auth/v1/token?grant_type=refresh_token",
            headers={"apikey": _secret("SUPABASE_ANON_KEY"), "Content-Type": "application/json"},
            json={"refresh_token": refresh_token},
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()
        session["access_token"] = data["access_token"]
        session["refresh_token"] = data.get("refresh_token", refresh_token)
        session["expires_at"] = time.time() + int(data.get("expires_in", 3600))
        st.session_state.auth = session
        return True
    except (requests.RequestException, KeyError, ValueError):
        return False


def current_auth() -> dict:
    session = st.session_state.get("auth", {})
    if not session:
        return {}
    if not refresh_session():
        sign_out()
        return {}
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
