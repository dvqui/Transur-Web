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
    # Inyectamos estilos específicos para centrar y estructurar el login como tarjeta tipo SaaS
    st.markdown(
        f"""
        <style>
        .login-wrapper {{
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 80vh;
        }}
        .login-card {{
            background: #FFFFFF;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(11, 61, 102, 0.08);
            border: 1px solid {COLORS['gris_borde']};
            width: 100%;
            max-width: 440px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Creamos columnas para centrar la tarjeta de forma milimétrica en cualquier pantalla
    _, col_centro, _ = st.columns([1, 1.2, 1])
    
    with col_centro:
        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        # Encabezado con Logo y Títulos integrados simétricamente
        cols_logo = st.columns([1, 3])
        with cols_logo[0]:
            try:
                st.image(LOGO_PATH, width=65)
            except Exception:
                st.markdown("### 🚌")
        with cols_logo[1]:
            st.markdown(
                f"""
                <h4 style='color:{COLORS['azul_profundo']}; margin: 0; font-weight: 800; line-height: 1.2;'>Transur 7 de Mayo</h4>
                <p style='color:#5A6B7B; font-size: 12px; margin: 0;'>Gestión de Repuestos</p>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<hr style='margin: 20px 0; border: none; border-top: 1px solid #E5E7EB;'>", unsafe_allow_html=True)

        # Formulario limpio de acceso
        with st.form("form_login"):
            usuario_input = st.text_input("Usuario de acceso")
            password_input = st.text_input("Contraseña", type="password")
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
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

        st.markdown('</div>', unsafe_allow_html=True)


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

    if st.session_state["pagina"] in ("usuarios", "reportes") and st.session_state["usuario"]["rol"] != "Administrador":
        st.warning("No tienes permisos para ver esta sección.")
        st.session_state["pagina"] = "dashboard"
        render_fn = dashboard.render

    render_fn()


if __name__ == "__main__":
    main()
