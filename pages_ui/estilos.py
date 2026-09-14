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

        /* Sidebar institucional original */
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

        /* Botones generales */
        .stButton button, .stDownloadButton button {{
            background-color: {COLORS['azul_profundo']};
            color: #FFFFFF !important;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }}
        .stButton button p, .stButton button span, .stButton button div,
        .stDownloadButton button p, .stDownloadButton button span, .stDownloadButton button div {{
            color: #FFFFFF !important;
        }}
        .stButton button:hover, .stDownloadButton button:hover {{
            background-color: {COLORS['azul_oscuro']};
            color: #FFFFFF !important;
        }}
        
        .stButton button[kind="secondary"] {{
            background-color: {COLORS['rojo']};
        }}
        .stButton button[kind="secondary"]:hover {{
            background-color: {COLORS['rojo_hover']};
        }}

        /* Inputs limpios */
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
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, {COLORS['azul_profundo']} 0%, {COLORS['azul_medio']} 100%);
            padding: 14px 24px;
            border-radius: 12px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: {('none' if subtitulo == 'Inicio de sesión' else '0 2px 8px rgba(11,61,102,0.25)')};
        ">
            <div>
                <span style="color:#FFFFFF; font-size:20px; font-weight:800;">🚍 Transur 7 de Mayo</span>
                <span style="color:{COLORS['celeste']}; font-size:13px; margin-left:12px;">{subtitulo}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
