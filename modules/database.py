from __future__ import annotations

from typing import Any

import pandas as pd
import requests
import streamlit as st


def _secret(name: str) -> str:
    try:
        return str(st.secrets[name]).strip()
    except Exception:
        return ""


def _headers(admin: bool = False, prefer: str | None = None) -> dict:
    key = (
        _secret("SUPABASE_SERVICE_ROLE_KEY")
        if admin
        else _secret("SUPABASE_ANON_KEY")
    )

    headers = {
        "apikey": key,
        "Content-Type": "application/json",
    }

    # La clave sb_secret se envía solamente como apikey.
    # El usuario conectado utiliza su token para aplicar los permisos RLS.
    if not admin:
        token = st.session_state.get("auth", {}).get("access_token")
        if token:
            headers["Authorization"] = f"Bearer {token}"

    if prefer:
        headers["Prefer"] = prefer

    return headers


def _endpoint(table: str) -> str:
    return f"{_secret('SUPABASE_URL')}/rest/v1/{table}"


def select(table: str, params: dict | None = None, admin: bool = False) -> pd.DataFrame:
    query = {"select": "*"}
    query.update(params or {})
    try:
        response = requests.get(_endpoint(table), headers=_headers(admin), params=query, timeout=25)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as exc:
        st.error(f"No se pudo leer {table}: {exc}")
        return pd.DataFrame()


def insert(table: str, data: dict | list[dict], admin: bool = False) -> tuple[bool, str]:
    try:
        response = requests.post(
            _endpoint(table), headers=_headers(admin, "return=representation"), json=data, timeout=25
        )
        response.raise_for_status()
        return True, "Registro guardado correctamente."
    except requests.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        return False, f"No se pudo guardar: {detail[:240]}"
    except Exception as exc:
        return False, f"No se pudo guardar: {exc}"


def update(table: str, record_id: Any, data: dict, admin: bool = False) -> tuple[bool, str]:
    try:
        response = requests.patch(
            _endpoint(table),
            headers=_headers(admin, "return=minimal"),
            params={"id": f"eq.{record_id}"},
            json=data,
            timeout=25,
        )
        response.raise_for_status()
        return True, "Registro actualizado."
    except Exception as exc:
        return False, f"No se pudo actualizar: {exc}"


def delete(table: str, record_id: Any, admin: bool = False) -> tuple[bool, str]:
    try:
        response = requests.delete(
            _endpoint(table), headers=_headers(admin), params={"id": f"eq.{record_id}"}, timeout=25
        )
        response.raise_for_status()
        return True, "Registro eliminado."
    except Exception as exc:
        return False, f"No se pudo eliminar: {exc}"


def get_profile(user_id: str) -> dict:
    df = select("profiles", {"id": f"eq.{user_id}", "limit": "1"})
    if df.empty:
        return {}
    return df.iloc[0].to_dict()


def upload_evidence(file, user_id: str) -> tuple[bool, str]:
    if file is None:
        return True, ""
    url = _secret("SUPABASE_URL")
    key = _secret("SUPABASE_ANON_KEY")
    token = st.session_state.get("auth", {}).get("access_token", key)
    safe_name = file.name.replace(" ", "_")
    path = f"{user_id}/{pd.Timestamp.utcnow().strftime('%Y%m%d%H%M%S')}_{safe_name}"
    try:
        response = requests.post(
            f"{url}/storage/v1/object/evidencias/{path}",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {token}",
                "Content-Type": file.type or "application/octet-stream",
                "x-upsert": "false",
            },
            data=file.getvalue(),
            timeout=40,
        )
        response.raise_for_status()
        return True, f"{url}/storage/v1/object/public/evidencias/{path}"
    except Exception as exc:
        return False, f"No se pudo subir la evidencia: {exc}"

