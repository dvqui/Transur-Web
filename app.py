"""
Sistema de Gestión de Repuestos - Cooperativa de Transportes "Transur 7 de Mayo"
Versión web (Streamlit + PostgreSQL/Neon).
"""
import streamlit as st

from config import APP_NAME, LOGO_PATH, COLORS
from database.connection import inicializar_bd
from services.auth_service import AuthService, AuthError
from pages_ui.estilos import inyectar_estilos, banner_institucional
from pages_ui import dashboard, inventario, usuarios, ventas, pagos, reportes

st.set_page_config(page_title=APP_NAME, page_icon="🚌", layout="wide")
inyectar_estilos()

# --- Inicializa el esquema y datos base en Neon (una sola vez) -----------------
try:
    inicializar_bd()
except Exception as e:
    st.error(
        "No se pudo conectar a la base de datos. Verifica que DATABASE_URL esté "
        "correctamente configurado en Secrets.\n\n"
        f"Detalle técnico: {e}"
    )
    st.stop()

if "usuario" not in st.session_state:
    st.session_state["usuario"] = None
if "pagina" not in st.session_state:
    st.session_state["pagina"] = "dashboard"


@st.dialog("Cambiar Contraseña")
def _dialogo_cambiar_password(obligatorio=False):
    auth = AuthService()
    if obligatorio:
        st.warning("Por seguridad, debes cambiar tu contraseña temporal antes de continuar.")

    actual = st.text_input("Contraseña actual", type="password", key="pwd_actual")
    nueva = st.text_input("Nueva contraseña", type="password", key="pwd_nueva")
    confirmar = st.text_input("Confirmar nueva contraseña", type="password", key="pwd_confirmar")

    if st.button("Guardar", use_container_width=True):
        if nueva != confirmar:
            st.error("Las contraseñas nuevas no coinciden.")
            return
        try:
            auth.cambiar_password(st.session_state["usuario"]["id_usuario"], actual, nueva)
            st.session_state["usuario"]["requiere_cambio_pwd"] = False
            st.success("Contraseña actualizada correctamente.")
            st.rerun()
        except AuthError as e:
            st.error(str(e))


def _pantalla_login():
    # Espaciado superior para centrar elegantemente la tarjeta en la pantalla
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_izq, col_centro, col_der = st.columns([1, 1.1, 1])
    with col_centro:
        st.markdown(
            f"""<div class="transur-card" style="text-align:center; padding: 45px 35px;
            border-top: 6px solid {COLORS['azul_profundo']};">""",
            unsafe_allow_html=True,
        )
        try:
            st.image(LOGO_PATH, width=100)
        except Exception:
            st.markdown("### 🚌")

        st.markdown(
            "<h2 style='color:#0B3D66; margin-bottom: 0; font-weight: 800;'>Transur 7 de Mayo</h2>"
            "<p style='color:#5A6B7B; margin-top: 4px; font-size: 14px; font-weight: 500;'>Sistema de Gestión de Repuestos</p>",
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        with st.form("form_login"):
            usuario_input = st.text_input("Usuario")
            password_input = st.text_input("Contraseña", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            enviar = st.form_submit_button("Iniciar Sesión", use_container_width=True)

        if enviar:
            if not usuario_input or not password_input:
                st.error("Por favor complete usuario y contraseña.")
            else:
                try:
                    auth = AuthService()
                    datos = auth.login(usuario_input.strip(), password_input)
                    st.session_state["usuario"] = datos
                    st.rerun()
                except AuthError as e:
                    st.error(str(e))

        st.markdown("</div>", unsafe_allow_html=True)


def _sidebar():
    usuario = st.session_state["usuario"]
    with st.sidebar:
        try:
            st.image(LOGO_PATH, width=70)
        except Exception:
            pass
        st.markdown(f"### Transur 7 de Mayo")
        st.caption("Gestión de Repuestos")
        st.divider()

        opciones = [
            ("dashboard", "🏠  Dashboard"),
            ("inventario", "📦  Inventario"),
            ("ventas", "🧾  Ventas"),
            ("pagos", "💳  Pagos"),
        ]
        if usuario["rol"] == "Administrador":
            opciones.append(("usuarios", "👥  Usuarios y Socios"))
            opciones.append(("reportes", "📊  Reportes Excel"))

        for clave, texto in opciones:
            if st.button(texto, key=f"nav_{clave}", use_container_width=True):
                st.session_state["pagina"] = clave
                st.rerun()

        st.divider()
        st.markdown(f"**{usuario['nombres']} {usuario['apellidos']}**")
        st.caption(usuario["rol"])

        if st.button("🔑 Cambiar contraseña", use_container_width=True):
            _dialogo_cambiar_password(obligatorio=False)

        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state["usuario"] = None
            st.session_state["pagina"] = "dashboard"
            st.rerun()


def main():
    if st.session_state["usuario"] is None:
        _pantalla_login()
        return

    _sidebar()
    banner_institucional()

    if st.session_state["usuario"].get("requiere_cambio_pwd"):
        _dialogo_cambiar_password(obligatorio=True)

    paginas = {
        "dashboard": dashboard.render,
        "inventario": inventario.render,
        "ventas": ventas.render,
        "pagos": pagos.render,
        "usuarios": usuarios.render,
        "reportes": reportes.render,
    }
    render_fn = paginas.get(st.session_state["pagina"], dashboard.render)

    # Protección de rutas restringidas a Administrador (por si se manipula el estado)
    if st.session_state["pagina"] in ("usuarios", "reportes") and st.session_state["usuario"]["rol"] != "Administrador":
        st.warning("No tienes permisos para ver esta sección.")
        st.session_state["pagina"] = "dashboard"
        render_fn = dashboard.render

    render_fn()


if __name__ == "__main__":
    main()
