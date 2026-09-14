"""CSS institucional inyectado en la app (paleta azul/blanco/rojo/celeste)."""
import streamlit as st
from config import COLORS


def inyectar_estilos():
    st.markdown(
        f"""
        <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        .stApp {{
            background-color: {COLORS['gris_fondo']};
        }}

        /* Sidebar institucional */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['azul_profundo']};
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['blanco']} !important;
        }}
        section[data-testid="stSidebar"] .stButton button {{
            background-color: transparent;
            border: none;
            text-align: left;
            font-weight: 500;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background-color: {COLORS['azul_medio']};
            color: {COLORS['blanco']} !important;
        }}

        /* Botones principales - Forzar texto blanco nítido */
        .stButton button, .stDownloadButton button, div[data-testid="stFormSubmitButton"] button {{
            background-color: {COLORS['azul_profundo']} !important;
            color: #FFFFFF !important;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }}
        .stButton button *, .stDownloadButton button *, div[data-testid="stFormSubmitButton"] button * {{
            color: #FFFFFF !important;
        }}
        .stButton button:hover, .stDownloadButton button:hover, div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: {COLORS['azul_medio']} !important;
            color: #FFFFFF !important;
        }}

        /* Botones secundarios (Eliminar/Cancelar) en rojo */
        .stButton button[kind="secondary"] {{
            background-color: {COLORS['rojo']} !important;
        }}
        .stButton button[kind="secondary"] * {{
            color: #FFFFFF !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background-color: {COLORS['rojo_hover']} !important;
        }}

        /* Tarjetas limpias */
        .transur-card {{
            background-color: {COLORS['blanco']};
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid {COLORS['gris_borde']};
        }}

        /* Inputs y campos */
        .stTextInput input, .stNumberInput input, .stTextArea textarea {{
            background-color: {COLORS['blanco']} !important;
            color: {COLORS['texto_oscuro']} !important;
            border: 1px solid {COLORS['gris_borde']} !important;
            border-radius: 8px !important;
        }}
        
        .stApp label, .stApp p, .stApp span, .stApp .stMarkdown {{
            color: {COLORS['texto_oscuro']};
        }}
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{
            color: {COLORS['blanco']} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def banner_institucional(subtitulo: str = "Sistema de Gestión de Repuestos"):
    """Franja superior limpia y alineada correctamente."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['azul_profundo']} 0%, {COLORS['azul_medio']} 100%);
            padding: 16px 24px;
            border-radius: 10px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: {('none' if subtirulo == 'Inicio de sesión' else '0 4px 12px rgba(11,61,102,0.15)')};
        ">
            <div style="display: flex; align-items: baseline; gap: 12px;">
                <span style="color:#FFFFFF; font-size:20px; font-weight:800;">🚍 Transur 7 de Mayo</span>
                <span style="color:{COLORS['celeste']}; font-size:13px; font-weight:500;">{subtitulo}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
