"""
Conexión a PostgreSQL (pensado para Neon, pero funciona con cualquier
Postgres). Lee la cadena de conexión desde st.secrets["DATABASE_URL"]
(Streamlit Cloud) o desde la variable de entorno DATABASE_URL (local/otros
hosts), en ese orden.
"""
import os
import streamlit as st
import psycopg2
import psycopg2.extras

from utils.security import generar_salt, hash_password
from config import ROLE_ADMIN, ROLE_SOCIO, ROLE_CLIENTE

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema_postgres.sql")


def _obtener_url_conexion() -> str:
    try:
        if "DATABASE_URL" in st.secrets:
            return st.secrets["DATABASE_URL"]
    except Exception:
        pass
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "No se encontró DATABASE_URL. Configúrala en .streamlit/secrets.toml "
            "(local) o en 'Secrets' dentro de Streamlit Community Cloud."
        )
    return url


@st.cache_resource(show_spinner=False)
def obtener_conexion():
    """Conexión reutilizada durante la vida de la app (cacheada por Streamlit)."""
    url = _obtener_url_conexion()
    conn = psycopg2.connect(url, sslmode="require")
    conn.autocommit = True
    return conn


def ejecutar(query: str, params: tuple = ()):
    conn = obtener_conexion()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur


def ejecutar_retornando(query: str, params: tuple = ()):
    """Para INSERT ... RETURNING id, útil para obtener el id autogenerado."""
    conn = obtener_conexion()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()


def consultar(query: str, params: tuple = ()) -> list:
    conn = obtener_conexion()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()


def consultar_uno(query: str, params: tuple = ()):
    conn = obtener_conexion()
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchone()


@st.cache_resource(show_spinner=False)
def inicializar_bd():
    """Crea el esquema (si no existe) y siembra los datos base. Se ejecuta
    una sola vez por instancia de la app gracias al cache_resource."""
    conn = obtener_conexion()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    with conn.cursor() as cur:
        cur.execute(schema_sql)

    # --- Sembrar roles ---------------------------------------------------
    for rol, desc in [
        (ROLE_ADMIN, "Acceso total al sistema"),
        (ROLE_SOCIO, "Miembro activo de la cooperativa"),
        (ROLE_CLIENTE, "Cliente externo con acceso restringido"),
    ]:
        ejecutar(
            "INSERT INTO roles (nombre_rol, descripcion) VALUES (%s, %s) "
            "ON CONFLICT (nombre_rol) DO NOTHING",
            (rol, desc),
        )

    # --- Sembrar usuario administrador por defecto ------------------------
    existe_admin = consultar_uno("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s", ("admin",))
    if not existe_admin:
        id_rol_admin = consultar_uno(
            "SELECT id_rol FROM roles WHERE nombre_rol = %s", (ROLE_ADMIN,)
        )["id_rol"]
        salt = generar_salt()
        password_hash = hash_password("admin123", salt)
        ejecutar(
            """
            INSERT INTO usuarios
                (nombres, apellidos, cedula, correo_electronico, telefono, direccion,
                 nombre_usuario, password_hash, password_salt, id_rol, activo,
                 requiere_cambio_pwd)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE, TRUE)
            """,
            (
                "Administrador", "del Sistema", "0000000000",
                "admin@transur7demayo.com", "0999999999", "Oficina Central",
                "admin", password_hash, salt, id_rol_admin,
            ),
        )

    # --- Categorías demo ---------------------------------------------------
    for c in ["Frenos", "Motor", "Suspensión", "Eléctrico", "Carrocería"]:
        ejecutar("INSERT INTO categorias (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (c,))

    return True
