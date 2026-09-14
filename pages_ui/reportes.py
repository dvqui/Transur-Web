"""Página: Reportes en Excel (descarga directa, sin guardar en el servidor)."""
import streamlit as st

from services.inventario_service import InventarioService
from services.venta_service import VentaService
from services.pago_service import PagoService
from services.export_service import generar_reporte_excel


def render():
    st.markdown("### 📊 Reportes en Excel")
    st.caption("Genera reportes profesionales (.xlsx) listos para imprimir o compartir.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """<div class="transur-card" style="text-align:center;">
            <div style="font-size:36px;">📦</div>
            <b>Inventario de Repuestos</b>
            <p style="color:#5A6B7B;font-size:12px;">Código, nombre, categoría, precios y stock.</p>
            </div>""",
            unsafe_allow_html=True,
        )
        inv = InventarioService()
        repuestos = inv.listar_repuestos()
        encabezados = ["Código", "Nombre", "Categoría", "Proveedor",
                       "Precio Compra", "Precio Venta", "Stock", "Stock Mínimo"]
        filas = [
            (r["codigo"], r["nombre"], r["nombre_categoria"] or "-", r["nombre_proveedor"] or "-",
             float(r["precio_compra"]), float(r["precio_venta"]), r["stock"], r["stock_minimo"])
            for r in repuestos
        ]
        excel_bytes = generar_reporte_excel(
            "Reporte de Inventario - Transur 7 de Mayo", encabezados, filas,
            columnas_moneda=[4, 5], nombre_hoja="Inventario",
        )
        st.download_button(
            "⬇ Exportar a Excel", data=excel_bytes, file_name="reporte_inventario.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col2:
        st.markdown(
            """<div class="transur-card" style="text-align:center;">
            <div style="font-size:36px;">🧾</div>
            <b>Ventas</b>
            <p style="color:#5A6B7B;font-size:12px;">Historial de ventas con cliente, fecha y total.</p>
            </div>""",
            unsafe_allow_html=True,
        )
        venta_service = VentaService()
        ventas = venta_service.listar_ventas()
        encabezados = ["N° Venta", "Fecha", "Cliente", "Vendedor", "Total", "Estado"]
        filas = [
            (v["id_venta"], str(v["fecha_venta"]), v["cliente"], v["vendedor"],
             float(v["total"]), v["estado"])
            for v in ventas
        ]
        excel_bytes = generar_reporte_excel(
            "Reporte de Ventas - Transur 7 de Mayo", encabezados, filas,
            columnas_moneda=[4], nombre_hoja="Ventas",
        )
        st.download_button(
            "⬇ Exportar a Excel", data=excel_bytes, file_name="reporte_ventas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col3:
        st.markdown(
            """<div class="transur-card" style="text-align:center;">
            <div style="font-size:36px;">💳</div>
            <b>Pagos</b>
            <p style="color:#5A6B7B;font-size:12px;">Pagos recibidos, método y venta asociada.</p>
            </div>""",
            unsafe_allow_html=True,
        )
        pago_service = PagoService()
        pagos = pago_service.listar_pagos()
        encabezados = ["N° Pago", "N° Venta", "Fecha", "Cliente", "Monto", "Método", "Referencia"]
        filas = [
            (p["id_pago"], p["id_venta"], str(p["fecha_pago"]), p["cliente"],
             float(p["monto"]), p["metodo_pago"], p["referencia"] or "-")
            for p in pagos
        ]
        excel_bytes = generar_reporte_excel(
            "Reporte de Pagos - Transur 7 de Mayo", encabezados, filas,
            columnas_moneda=[4], nombre_hoja="Pagos",
        )
        st.download_button(
            "⬇ Exportar a Excel", data=excel_bytes, file_name="reporte_pagos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
