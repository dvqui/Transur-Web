"""Utilidad de paginación reutilizable para las tablas de cada módulo."""
import math
import streamlit as st


def paginar(datos: list, clave: str, filas_por_pagina: int = 8):
    """
    Devuelve el subconjunto de 'datos' correspondiente a la página actual
    y dibuja los controles de paginación (◀ Anterior / Siguiente ▶).
    'clave' debe ser única por tabla (ej. 'usuarios', 'inventario').
    """
    clave_pagina = f"pagina_{clave}"
    if clave_pagina not in st.session_state:
        st.session_state[clave_pagina] = 0

    total_paginas = max(1, math.ceil(len(datos) / filas_por_pagina))
    # Si el filtro cambió y la página quedó fuera de rango, la reiniciamos
    if st.session_state[clave_pagina] >= total_paginas:
        st.session_state[clave_pagina] = 0

    pagina_actual = st.session_state[clave_pagina]
    inicio = pagina_actual * filas_por_pagina
    fin = inicio + filas_por_pagina

    col_prev, col_info, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.button("◀ Anterior", key=f"prev_{clave}", disabled=(pagina_actual == 0)):
            st.session_state[clave_pagina] -= 1
            st.rerun()
    with col_info:
        st.markdown(
            f"<p style='text-align:center;font-weight:600;'>Página {pagina_actual + 1} de {total_paginas}"
            f" &nbsp;({len(datos)} registros)</p>",
            unsafe_allow_html=True,
        )
    with col_next:
        if st.button("Siguiente ▶", key=f"next_{clave}", disabled=(fin >= len(datos))):
            st.session_state[clave_pagina] += 1
            st.rerun()

    return datos[inicio:fin]
