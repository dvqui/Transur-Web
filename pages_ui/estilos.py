"""CSS institucional inyectado en la app (paleta azul/blanco/rojo/celeste)."""
import streamlit as st
from config import COLORS


def inyectar_estilos():
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        .stApp {{
            background-color: {COLORS['gris_fondo']};
            font-family: 'Plus Jakarta Sans', sans-serif, -apple-system;
        }}

        html, body, [class*="css"] {{
            font-family: 'Plus Jakarta Sans', sans-serif, -apple-system;
        }}

        /* ==========================================================
           1. SIDEBAR PROFESIONAL
           ========================================================== */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS['azul_profundo']} 0%, #061E38 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['blanco']} !important;
        }}
        section[data-testid="stSidebar"] div.stButton > button {{
            background-color: transparent !important;
            color: {COLORS['blanco']} !important;
            border: none !important;
            text-align: left !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            padding: 0.6rem 1rem !important;
            transition: all 0.2s ease-in-out;
        }}
        section[data-testid="stSidebar"] div.stButton > button:hover {{
            background-color: rgba(255, 255, 255, 0.12) !important;
            transform: translateX(4px);
        }}

        /* ==========================================================
           2. BOTONES GENERALES
           ========================================================== */
        .stMainBlockContainer div.stButton > button, 
        .stMainBlockContainer div.stDownloadButton > button, 
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, {COLORS['azul_profundo']} 0%, {COLORS['azul_medio']} 100%) !important;
            color: #FFFFFF !important;
            border-radius: 10px !important;
            border: none !important;
            font-weight: 600 !important;
            padding: 0.65rem 1.2rem !important;
            box-shadow: 0 4px 12px rgba(11, 61, 102, 0.2) !important;
            transition: all 0.25s ease !important;
        }}
        .stMainBlockContainer div.stButton > button *, 
        .stMainBlockContainer div.stDownloadButton > button *, 
        div[data-testid="stFormSubmitButton"] button * {{
            color: #FFFFFF !important;
        }}
        .stMainBlockContainer div.stButton > button:hover, 
        div[data-testid="stFormSubmitButton"] button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(11, 61, 102, 0.3) !important;
        }}

        .stMainBlockContainer div.stButton > button[kind="secondary"] {{
            background: linear-gradient(135deg, {COLORS['rojo']} 0%, {COLORS['rojo_hover']} 100%) !important;
            box-shadow: 0 4px 12px rgba(215, 38, 61, 0.2) !important;
        }}

        /* ==========================================================
           3. ETIQUETAS Y CAMPOS DE TEXTO EN LOGIN
           ========================================================== */
        /* Forzar color oscuro altamente visible en los labels del formulario */
        div[data-testid="stForm"] label p, 
        div[data-testid="stForm"] label span, 
        div[data-testid="stForm"] label,
        .stForm label {{
            color: #0F172A !important;
            font-weight: 700 !important;
            font-size: 14px !important;
        }}

        .stTextInput input, .stNumberInput input, .stTextArea textarea {{
            background-color: #F9FAFB !important;
            color: {COLORS['texto_oscuro']} !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 10px !important;
            padding: 12px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }}
        .stTextInput input:focus, .stNumberInput input:focus {{
            border-color: {COLORS['celeste']} !important;
            box-shadow: 0 0 0 4px rgba(41, 171, 226, 0.15) !important;
            background-color: #FFFFFF !important;
        }}

        .stApp label, .stApp p, .stApp span, .stApp .stMarkdown {{
            color: {COLORS['texto_oscuro']};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def banner_institucional(subtitulo: str = "Sistema de Gestión de Repuestos"):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['azul_profundo']} 0%, {COLORS['azul_medio']} 100%);
            padding: 20px 30px;
            border-radius: 14px;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 6px 20px rgba(11, 61, 102, 0.12);
        ">
            <div style="display: flex; align-items: baseline; gap: 14px;">
                <span style="color:#FFFFFF; font-size:22px; font-weight:800; letter-spacing:-0.5px;">🚍 Transur 7 de Mayo</span>
                <span style="color:{COLORS['celeste']}; font-size:14px; font-weight:500; border-left: 2px solid rgba(255,255,255,0.25); padding-left: 14px;">{subtitulo}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
