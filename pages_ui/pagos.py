"""Página: Pagos."""
import streamlit as st

from services.pago_service import PagoService, PagoServiceError
from services.venta_service import VentaService
from pages_ui.componentes import paginar


@st.dialog("Registrar Pago")
def _modal_nuevo_pago(pago_service: PagoService, venta_service: VentaService):
    ventas_pendientes = [v for v in venta_service.listar_ventas() if v["estado"] != "PAGADA"]
    if not ventas_pendientes:
        st.info("No hay ventas pendientes de pago.")
        return

    opciones_venta = [
        f"Venta N°{v['id_venta']} - {v['cliente']} (${float(v['total']):.2f})"
        for v in ventas_pendientes
    ]
    venta_sel = st.selectbox("Venta", opciones_venta)
    idx = opciones_venta.index(venta_sel)
    id_venta = ventas_pendientes[idx]["id_venta"]
    saldo = pago_service.saldo_pendiente(id_venta)
    st.markdown(f"**Saldo pendiente: ${saldo:.2f}**")

    monto = st.number_input("Monto a pagar", min_value=0.0, step=1.0, format="%.2f")
    metodo = st.selectbox("Método de pago", ["EFECTIVO", "TRANSFERENCIA", "TARJETA"])
    referencia = st.text_input("Referencia / N° de comprobante (opcional)")

    if st.button("💾 Registrar Pago", use_container_width=True):
        if monto <= 0:
            st.error("Ingrese un monto válido.")
            return
        try:
            pago_service.registrar_pago(id_venta, monto, metodo, referencia.strip())
            st.success("Pago registrado correctamente.")
            st.session_state["_recargar_pagos"] = True
            st.rerun()
        except PagoServiceError as e:
            st.error(str(e))


def render():
    pago_service = PagoService()
    venta_service = VentaService()

    col_titulo, col_boton = st.columns([4, 1])
    with col_titulo:
        st.markdown("### 💳 Registro de Pagos")
    with col_boton:
        if st.button("+ Registrar Pago", use_container_width=True):
            _modal_nuevo_pago(pago_service, venta_service)

    filtro = st.text_input("🔍 Buscar por cliente o método de pago", key="filtro_pagos")
    pagos = pago_service.listar_pagos(filtro)

    if not pagos:
        st.info("No se encontraron pagos.")
        return

    pagina = paginar(pagos, "pagos", filas_por_pagina=8)

    for p in pagina:
        st.markdown(
            f"""<div class="transur-card" style="margin-bottom:8px;padding:14px 18px;">
            <b>Pago N°{p['id_pago']}</b> — Venta N°{p['id_venta']} · {p['cliente']}<br/>
            <span style="color:#5A6B7B;">{str(p['fecha_pago'])[:16]} &nbsp;|&nbsp;
            Monto: ${float(p['monto']):.2f} &nbsp;|&nbsp; {p['metodo_pago']}
            {'&nbsp;|&nbsp; Ref: ' + p['referencia'] if p['referencia'] else ''}</span>
            </div>""",
            unsafe_allow_html=True,
        )
