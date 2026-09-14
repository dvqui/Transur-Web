"""Página: Dashboard general."""
import streamlit as st

from services.inventario_service import InventarioService
from services.venta_service import VentaService
from services.usuario_service import UsuarioService


def render():
    usuario = st.session_state["usuario"]
    st.markdown(f"### Bienvenido/a, {usuario['nombres']} {usuario['apellidos']} 👋")
    st.caption("Panel general del sistema de repuestos")

    inv = InventarioService()
    venta_service = VentaService()
    usr_service = UsuarioService()

    repuestos = inv.listar_repuestos()
    bajo_stock = inv.repuestos_bajo_stock()
    ventas = venta_service.listar_ventas()
    usuarios = usr_service.listar_usuarios()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Repuestos en inventario", len(repuestos))
    col2.metric("⚠️ Repuestos con stock bajo", len(bajo_stock))
    col3.metric("🧾 Ventas registradas", len(ventas))
    col4.metric("👥 Usuarios del sistema", len(usuarios))

    if bajo_stock:
        st.markdown(
            f"""<div class="transur-alert-warning">⚠️ Hay {len(bajo_stock)} repuesto(s)
            con stock igual o menor al mínimo. Revisa el módulo de Inventario.</div>""",
            unsafe_allow_html=True,
        )

    st.markdown("#### Accesos rápidos")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("📦 Ver Inventario", use_container_width=True):
            st.session_state["pagina"] = "inventario"
            st.rerun()
    with c2:
        if st.button("🧾 Registrar Venta", use_container_width=True):
            st.session_state["pagina"] = "ventas"
            st.rerun()
    with c3:
        if st.button("💳 Registrar Pago", use_container_width=True):
            st.session_state["pagina"] = "pagos"
            st.rerun()
    with c4:
        if usuario["rol"] == "Administrador":
            if st.button("👥 Gestionar Usuarios", use_container_width=True):
                st.session_state["pagina"] = "usuarios"
                st.rerun()
