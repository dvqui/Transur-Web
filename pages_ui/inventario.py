"""Página: Inventario de Repuestos."""
import streamlit as st

from services.inventario_service import InventarioService, InventarioServiceError
from utils.validators import validar_no_vacio
from pages_ui.componentes import paginar


@st.dialog("Nuevo Repuesto")
def _modal_crear(service: InventarioService):
    categorias = service.listar_categorias()
    nombres_cat = [c["nombre"] for c in categorias] or ["General"]
    proveedores = service.listar_proveedores()
    nombres_prov = ["(Sin proveedor)"] + [p["nombre"] for p in proveedores]

    codigo = st.text_input("Código *")
    nombre = st.text_input("Nombre *")
    descripcion = st.text_area("Descripción", height=70)
    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Categoría", nombres_cat)
    with col2:
        proveedor = st.selectbox("Proveedor", nombres_prov)
    col3, col4 = st.columns(2)
    with col3:
        precio_compra = st.number_input("Precio de compra", min_value=0.0, step=0.5, format="%.2f")
        stock = st.number_input("Stock inicial", min_value=0, step=1)
    with col4:
        precio_venta = st.number_input("Precio de venta", min_value=0.0, step=0.5, format="%.2f")
        stock_minimo = st.number_input("Stock mínimo (alerta)", min_value=0, step=1, value=5)

    if st.button("💾 Guardar Repuesto", use_container_width=True):
        if not (validar_no_vacio(codigo) and validar_no_vacio(nombre)):
            st.error("Código y nombre son obligatorios.")
            return
        id_cat = next((c["id_categoria"] for c in categorias if c["nombre"] == categoria), None)
        id_prov = next((p["id_proveedor"] for p in proveedores if p["nombre"] == proveedor), None)
        try:
            service.crear_repuesto(
                codigo.strip(), nombre.strip(), descripcion.strip(), id_cat, id_prov,
                precio_compra, precio_venta, int(stock), int(stock_minimo),
            )
            st.success("Repuesto agregado correctamente.")
            st.session_state["_recargar_inventario"] = True
            st.rerun()
        except InventarioServiceError as e:
            st.error(str(e))


@st.dialog("Editar Repuesto")
def _modal_editar(service: InventarioService, id_repuesto: int):
    rep = service.obtener_repuesto(id_repuesto)
    if rep is None:
        st.error("El repuesto no existe.")
        return

    categorias = service.listar_categorias()
    nombres_cat = [c["nombre"] for c in categorias] or ["General"]
    cat_actual = next((c["nombre"] for c in categorias if c["id_categoria"] == rep["id_categoria"]), None)

    proveedores = service.listar_proveedores()
    nombres_prov = ["(Sin proveedor)"] + [p["nombre"] for p in proveedores]
    prov_actual = next((p["nombre"] for p in proveedores if p["id_proveedor"] == rep["id_proveedor"]), "(Sin proveedor)")

    codigo = st.text_input("Código *", rep["codigo"])
    nombre = st.text_input("Nombre *", rep["nombre"])
    descripcion = st.text_area("Descripción", rep["descripcion"] or "", height=70)
    col1, col2 = st.columns(2)
    with col1:
        categoria = st.selectbox("Categoría", nombres_cat, index=nombres_cat.index(cat_actual) if cat_actual in nombres_cat else 0)
    with col2:
        proveedor = st.selectbox("Proveedor", nombres_prov, index=nombres_prov.index(prov_actual) if prov_actual in nombres_prov else 0)
    col3, col4 = st.columns(2)
    with col3:
        precio_compra = st.number_input("Precio de compra", min_value=0.0, step=0.5, value=float(rep["precio_compra"]), format="%.2f")
        stock = st.number_input("Stock actual", min_value=0, step=1, value=int(rep["stock"]))
    with col4:
        precio_venta = st.number_input("Precio de venta", min_value=0.0, step=0.5, value=float(rep["precio_venta"]), format="%.2f")
        stock_minimo = st.number_input("Stock mínimo", min_value=0, step=1, value=int(rep["stock_minimo"]))

    col_guardar, col_eliminar = st.columns(2)
    with col_guardar:
        if st.button("💾 Guardar Cambios", use_container_width=True):
            id_cat = next((c["id_categoria"] for c in categorias if c["nombre"] == categoria), None)
            id_prov = next((p["id_proveedor"] for p in proveedores if p["nombre"] == proveedor), None)
            try:
                service.actualizar_repuesto(
                    rep["id_repuesto"], codigo.strip(), nombre.strip(), descripcion.strip(),
                    id_cat, id_prov, precio_compra, precio_venta, int(stock), int(stock_minimo),
                )
                st.success("Repuesto actualizado.")
                st.session_state["_recargar_inventario"] = True
                st.rerun()
            except InventarioServiceError as e:
                st.error(str(e))
    with col_eliminar:
        if st.button("🗑️ Eliminar", use_container_width=True, type="secondary"):
            service.eliminar_repuesto(rep["id_repuesto"])
            st.success("Repuesto eliminado.")
            st.session_state["_recargar_inventario"] = True
            st.rerun()


def render():
    usuario = st.session_state["usuario"]
    service = InventarioService()

    col_titulo, col_boton = st.columns([4, 1])
    with col_titulo:
        st.markdown("### 📦 Inventario de Repuestos")
    with col_boton:
        if usuario["rol"] == "Administrador":
            if st.button("+ Nuevo Repuesto", use_container_width=True):
                _modal_crear(service)

    filtro = st.text_input("🔍 Buscar por código o nombre", key="filtro_inventario")
    repuestos = service.listar_repuestos(filtro)

    if not repuestos:
        st.info("No se encontraron repuestos.")
        return

    pagina = paginar(repuestos, "inventario", filas_por_pagina=8)

    for r in pagina:
        estado = "⚠️ Stock bajo" if r["stock"] <= r["stock_minimo"] else "✅ Normal"
        col_info, col_accion = st.columns([5, 1])
        with col_info:
            st.markdown(
                f"""<div class="transur-card" style="margin-bottom:8px;padding:14px 18px;">
                <b>{r['codigo']}</b> — {r['nombre']} &nbsp;|&nbsp; Categoría: {r['nombre_categoria'] or '-'}
                &nbsp;|&nbsp; Precio: ${float(r['precio_venta']):.2f} &nbsp;|&nbsp; Stock: {r['stock']} {estado}
                </div>""",
                unsafe_allow_html=True,
            )
        with col_accion:
            if usuario["rol"] == "Administrador":
                if st.button("✏️ Editar", key=f"edit_rep_{r['id_repuesto']}"):
                    _modal_editar(service, r["id_repuesto"])
