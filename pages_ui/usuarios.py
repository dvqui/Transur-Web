"""Página: Usuarios, Socios y Clientes Externos."""
import streamlit as st

from config import ROLES
from services.usuario_service import UsuarioService, UsuarioServiceError
from services.auth_service import AuthService
from utils.validators import validar_no_vacio, validar_password_segura
from pages_ui.componentes import paginar


@st.dialog("Nuevo Usuario")
def _modal_crear(service: UsuarioService):
    col1, col2 = st.columns(2)
    with col1:
        nombres = st.text_input("Nombres *")
        cedula = st.text_input("Cédula / Identificación")
        telefono = st.text_input("Teléfono")
        nombre_usuario = st.text_input("Nombre de usuario (login) *")
    with col2:
        apellidos = st.text_input("Apellidos *")
        correo = st.text_input("Correo electrónico *")
        direccion = st.text_input("Dirección")
        password = st.text_input("Contraseña inicial *", type="password")

    rol = st.selectbox("Rol *", ROLES)

    if st.button("💾 Guardar Usuario", use_container_width=True):
        campos = [nombres, apellidos, correo, nombre_usuario, password]
        if not all(validar_no_vacio(c) for c in campos):
            st.error("Complete todos los campos obligatorios (*).")
            return
        valida, msg = validar_password_segura(password)
        if not valida:
            st.error(msg)
            return
        try:
            service.crear_usuario(
                nombres.strip(), apellidos.strip(), cedula.strip(), correo.strip(),
                telefono.strip(), direccion.strip(), nombre_usuario.strip(), password, rol,
            )
            st.success("Usuario creado correctamente.")
            st.session_state["_recargar_usuarios"] = True
            st.rerun()
        except UsuarioServiceError as e:
            st.error(str(e))


@st.dialog("Editar Usuario")
def _modal_editar(service: UsuarioService, auth_service: AuthService, id_usuario: int):
    u = service.obtener_usuario(id_usuario)
    if u is None:
        st.error("El usuario no existe.")
        return

    col1, col2 = st.columns(2)
    with col1:
        nombres = st.text_input("Nombres *", u["nombres"])
        cedula = st.text_input("Cédula", u["cedula"] or "")
        telefono = st.text_input("Teléfono", u["telefono"] or "")
    with col2:
        apellidos = st.text_input("Apellidos *", u["apellidos"])
        correo = st.text_input("Correo electrónico *", u["correo_electronico"])
        direccion = st.text_input("Dirección", u["direccion"] or "")

    rol = st.selectbox("Rol *", ROLES, index=ROLES.index(u["nombre_rol"]) if u["nombre_rol"] in ROLES else 0)

    if st.button("💾 Guardar Cambios", use_container_width=True):
        if not all(validar_no_vacio(c) for c in [nombres, apellidos, correo]):
            st.error("Complete todos los campos obligatorios (*).")
            return
        try:
            service.actualizar_usuario(
                u["id_usuario"], nombres.strip(), apellidos.strip(), cedula.strip(),
                correo.strip(), telefono.strip(), direccion.strip(), rol,
            )
            st.success("Usuario actualizado correctamente.")
            st.session_state["_recargar_usuarios"] = True
            st.rerun()
        except UsuarioServiceError as e:
            st.error(str(e))

    st.divider()
    st.markdown("**🔐 Zona de administrador**")

    col_estado, col_reset = st.columns(2)
    activo_actual = bool(u["activo"])
    with col_estado:
        texto_btn = "🚫 Deshabilitar" if activo_actual else "✅ Habilitar"
        if st.button(texto_btn, use_container_width=True):
            service.cambiar_estado(u["id_usuario"], not activo_actual)
            st.success("Estado actualizado.")
            st.session_state["_recargar_usuarios"] = True
            st.rerun()
    with col_reset:
        if st.button("🔑 Restablecer contraseña", use_container_width=True):
            if u["id_usuario"] == st.session_state["usuario"]["id_usuario"]:
                st.warning("Usa 'Cambiar mi contraseña' en el menú lateral.")
            else:
                temp_pwd = auth_service.resetear_password_admin(
                    u["id_usuario"], st.session_state["usuario"]["id_usuario"]
                )
                st.success(
                    f"Contraseña temporal para **{u['nombre_usuario']}**: `{temp_pwd}`\n\n"
                    f"Debe cambiarla en su próximo inicio de sesión."
                )


def render():
    service = UsuarioService()
    auth_service = AuthService()

    col_titulo, col_boton = st.columns([4, 1])
    with col_titulo:
        st.markdown("### 👥 Usuarios, Socios y Clientes")
    with col_boton:
        if st.button("+ Nuevo Usuario", use_container_width=True):
            _modal_crear(service)

    col_filtro, col_rol = st.columns([3, 1])
    with col_filtro:
        filtro = st.text_input("🔍 Buscar por nombre, correo o cédula", key="filtro_usuarios")
    with col_rol:
        rol_filtro = st.selectbox("Rol", ["Todos"] + ROLES)

    usuarios = service.listar_usuarios(filtro, None if rol_filtro == "Todos" else rol_filtro)

    if not usuarios:
        st.info("No se encontraron usuarios.")
        return

    pagina = paginar(usuarios, "usuarios", filas_por_pagina=8)

    for u in pagina:
        estado = "✅ Activo" if u["activo"] else "🚫 Inactivo"
        col_info, col_accion = st.columns([5, 1])
        with col_info:
            st.markdown(
                f"""<div class="transur-card" style="margin-bottom:8px;padding:14px 18px;">
                <b>{u['nombres']} {u['apellidos']}</b> ({u['nombre_rol']}) — {estado}<br/>
                <span style="color:#5A6B7B;">✉️ {u['correo_electronico']} &nbsp;|&nbsp; usuario: {u['nombre_usuario']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        with col_accion:
            if st.button("✏️ Editar", key=f"edit_usr_{u['id_usuario']}"):
                _modal_editar(service, auth_service, u["id_usuario"])
