# Kaironix SSOMA 360

Aplicación web de control preventivo de flota desarrollada con **Python + Streamlit + Supabase**.

## Funciones incluidas

- Login seguro con correo y contraseña mediante Supabase Auth.
- Roles: Administrador, Inspector y Consulta.
- Registro maestro de unidades.
- Inspección preventiva con implementos y estado general.
- Carga de evidencias fotográficas.
- Registro, responsables y seguimiento de hallazgos.
- Dashboard con KPIs y gráficos.
- Filtros y reportes exportables a Excel.
- Diseño adaptable para computadora, celular y televisor.

## Privilegios

| Rol | Privilegios |
|---|---|
| Administrador | Acceso total, creación de cuentas y asignación de roles |
| Inspector | Registra unidades, inspecciones y hallazgos |
| Consulta | Visualiza dashboard, evidencias y reportes |

## 1. Crear la base de datos

1. Crea un proyecto gratuito en https://supabase.com.
2. Entra a **SQL Editor → New query**.
3. Copia todo el contenido de `supabase_setup.sql` y pulsa **Run**.
4. Entra a **Authentication → Users → Add user**.
5. Crea tu primera cuenta de administrador con correo y contraseña.
6. Copia el `UUID` del usuario creado.
7. Al final de `supabase_setup.sql` encontrarás un `INSERT` comentado. Reemplaza el UUID, nombre y correo; ejecútalo para crear tu perfil Administrador.

Ejemplo:

```sql
insert into public.profiles (id,nombre,email,rol,activo)
values ('UUID_REAL','Geerson Llaja Escalante','correo@ejemplo.com','Administrador',true);
```

## 2. Probar en tu computadora

Instala Python 3.11 o superior. Abre una terminal dentro del proyecto:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

Copia `.streamlit/secrets.example.toml` con el nombre `.streamlit/secrets.toml` y coloca las claves reales de Supabase.

Después ejecuta:

```bash
streamlit run app.py
```

Se abrirá `http://localhost:8501`.

## 3. Subir a GitHub

1. Crea un repositorio vacío llamado `kaironix-ssoma-360`.
2. Descomprime este ZIP.
3. En GitHub, pulsa **Add file → Upload files**.
4. Arrastra todo el contenido de la carpeta del proyecto.
5. Verifica que `app.py`, `requirements.txt`, `modules`, `.streamlit` y `supabase_setup.sql` estén visibles.
6. Pulsa **Commit changes**.

El archivo real `.streamlit/secrets.toml` no debe subirse. Está protegido por `.gitignore`.

## 4. Publicar gratis en Streamlit Community Cloud

1. Ingresa a https://share.streamlit.io con tu cuenta de GitHub.
2. Pulsa **Create app**.
3. Selecciona el repositorio y la rama `main`.
4. En **Main file path** escribe `app.py`.
5. En **Advanced settings → Secrets**, coloca:

```toml
SUPABASE_URL = "https://TU-PROYECTO.supabase.co"
SUPABASE_ANON_KEY = "TU_ANON_KEY"
SUPABASE_SERVICE_ROLE_KEY = "TU_SERVICE_ROLE_KEY"
```

6. Pulsa **Deploy**.

Streamlit generará un enlace similar a:

`https://kaironix-ssoma-360.streamlit.app`

## 5. Crear usuarios desde la aplicación

1. Ingresa con la cuenta Administrador.
2. Abre **Usuarios**.
3. Completa nombre, correo, contraseña temporal y rol.
4. Comparte con cada persona solo su propio correo y contraseña.

## Seguridad

- No guardes contraseñas en el código.
- No publiques la clave `SUPABASE_SERVICE_ROLE_KEY` en GitHub.
- Configura las claves únicamente en los Secrets de Streamlit.
- Las reglas RLS incluidas limitan las operaciones según el rol.
- Para uso empresarial formal, activa políticas internas de contraseñas y respaldo periódico.

## Estructura

```text
kaironix-ssoma-360/
├── app.py
├── requirements.txt
├── supabase_setup.sql
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.example.toml
└── modules/
    ├── __init__.py
    ├── auth.py
    ├── database.py
    └── styles.py
```

