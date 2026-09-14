"""Página: Ventas."""
import streamlit as st

from services.venta_service import VentaService, VentaServiceError
from services.inventario_service import InventarioService
from pages_ui.componentes import paginar


@st.dialog("Registrar Nueva Venta", width="large")
def _modal_nueva_venta(venta_service: VentaService, inv_service: InventarioService):
    if "carrito_venta" not in st.session_state:
        st.session_state["carrito_venta"] = []

    clientes = venta_service.clientes_y_socios()
    if not clientes:
        st.warning("No hay Socios/Clientes Externos registrados para vender.")
        return

    opciones_clientes = [f"{c['nombre_completo']} ({c['nombre_rol']})" for c in clientes]
    cliente_sel = st.selectbox("Cliente / Socio", opciones_clientes)

    repuestos = inv_service.listar_repuestos()
    if not repuestos:
        st.warning("No hay repuestos en inventario.")
        return
    opciones_rep = [f"{r['codigo']} - {r['nombre']} (Stock: {r['stock']})" for r in repuestos]

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        rep_sel = st.selectbox("Repuesto", opciones_rep)
    with col2:
        cantidad = st.number_input("Cantidad", min_value=1, step=1, value=1)
    with col3:
        st.write("")
        st.write("")
        agregar = st.button("➕ Agregar", use_container_width=True)

    if agregar:
        idx = opciones_rep.index(rep_sel)
        rep = repuestos[idx]
        if cantidad > rep["stock"]:
            st.error(f"Stock insuficiente (disponible: {rep['stock']}).")
        else:
            st.session_state["carrito_venta"].append({
                "id_repuesto": rep["id_repuesto"],
                "nombre": rep["nombre"],
                "cantidad": int(cantidad),
                "precio_unitario": float(rep["precio_venta"]),
                "subtotal": int(cantidad) * float(rep["precio_venta"]),
            })
            st.rerun()

    st.markdown("**Ítems agregados a la venta:**")
    total = 0.0
    for idx, item in enumerate(st.session_state["carrito_venta"]):
        total += item["subtotal"]
        c_item, c_quitar = st.columns([5, 1])
        with c_item:
            st.write(f"{item['nombre']} × {item['cantidad']} = ${item['subtotal']:.2f}")
        with c_quitar:
            if st.button("✕", key=f"quitar_{idx}"):
                st.session_state["carrito_venta"].pop(idx)
                st.rerun()

    st.markdown(f"### Total: ${total:.2f}")

    col_confirmar, col_cancelar = st.columns(2)
    with col_confirmar:
        if st.button("✅ Confirmar Venta", use_container_width=True):
            if not st.session_state["carrito_venta"]:
                st.error("Agregue al menos un repuesto a la venta.")
            else:
                idx_cliente = opciones_clientes.index(cliente_sel)
                id_cliente = clientes[idx_cliente]["id_usuario"]
                try:
                    venta_service.crear_venta(
                        id_cliente, st.session_state["usuario"]["id_usuario"],
                        st.session_state["carrito_venta"],
                    )
                    st.session_state["carrito_venta"] = []
                    st.success("Venta registrada correctamente.")
                    st.session_state["_recargar_ventas"] = True
                    st.rerun()
                except VentaServiceError as e:
                    st.error(str(e))
    with col_cancelar:
        if st.button("Cancelar", use_container_width=True):
            st.session_state["carrito_venta"] = []
            st.rerun()


@st.dialog("Detalle de Venta")
def _modal_detalle(venta_service: VentaService, id_venta: int):
    detalle = venta_service.detalle_venta(id_venta)
    for item in detalle:
        st.markdown(
            f"""**{item['nombre_repuesto']}** (Cód. {item['codigo']})
            Cantidad: {item['cantidad']} | P. Unitario: ${float(item['precio_unitario']):.2f}
            | Subtotal: ${float(item['subtotal']):.2f}"""
        )
        st.divider()


def render():
    venta_service = VentaService()
    inv_service = InventarioService()

    col_titulo, col_boton = st.columns([4, 1])
    with col_titulo:
        st.markdown("### 🧾 Registro de Ventas")
    with col_boton:
        if st.button("+ Nueva Venta", use_container_width=True):
            st.session_state["carrito_venta"] = []
            _modal_nueva_venta(venta_service, inv_service)

    filtro = st.text_input("🔍 Buscar por cliente o estado", key="filtro_ventas")
    ventas = venta_service.listar_ventas(filtro)

    if not ventas:
        st.info("No se encontraron ventas.")
        return

    pagina = paginar(ventas, "ventas", filas_por_pagina=8)

    iconos = {"PAGADA": "✅", "PENDIENTE": "🕒", "ANULADA": "🚫"}
    for v in pagina:
        icono = iconos.get(v["estado"], "")
        col_info, col_accion = st.columns([5, 1])
        with col_info:
            st.markdown(
                f"""<div class="transur-card" style="margin-bottom:8px;padding:14px 18px;">
                <b>Venta N°{v['id_venta']}</b> — {v['cliente']}<br/>
                <span style="color:#5A6B7B;">{str(v['fecha_venta'])[:16]} &nbsp;|&nbsp;
                Total: ${float(v['total']):.2f} &nbsp;|&nbsp; {icono} {v['estado']}</span>
                </div>""",
                unsafe_allow_html=True,
            )
        with col_accion:
            if st.button("👁️ Ver", key=f"ver_venta_{v['id_venta']}"):
                _modal_detalle(venta_service, v["id_venta"])
