"""CSS institucional inyectado en la app (paleta azul/blanco/rojo/celeste)."""
import streamlit as st
from config import COLORS


def inyectar_estilos():
    st.markdown(
        f"""
        <style>
        /* Oculta elementos por defecto de Streamlit para un look más limpio */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        /* Fondo general de la aplicación */
        .stApp {{
            background-color: {COLORS['gris_fondo']};
        }}

        /* Sidebar institucional */
        section[data-testid="stSidebar"] {{
            background-color: {COLORS['azul_profundo']};
            box-shadow: 2px 0 8px rgba(0,0,0,0.1);
        }}
        section[data-testid="stSidebar"] * {{
            color: {COLORS['blanco']} !important;
        }}
        
        /* Botones del Sidebar (Navegación) */
        section[data-testid="stSidebar"] .stButton button {{
            background-color: transparent;
            border: none;
            text-align: left;
            font-weight: 500;
            transition: all 0.2s ease-in-out;
            border-radius: 6px;
        }}
        section[data-testid="stSidebar"] .stButton button:hover {{
            background-color: rgba(255, 255, 255, 0.1); /* Efecto cristal */
            color: {COLORS['blanco']} !important;
            transform: translateX(4px); /* Pequeño salto a la derecha al pasar el mouse */
        }}

        /* Botones principales de acción */
        .stButton button, .stDownloadButton button {{
            background-color: {COLORS['azul_profundo']};
            color: #FFFFFF !important;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(11, 61, 102, 0.2);
        }}
        .stButton button p, .stButton button span, .stButton button div,
        .stDownloadButton button p, .stDownloadButton button span, .stDownloadButton button div {{
            color: #FFFFFF !important;
        }}
        .stButton button:hover, .stDownloadButton button:hover {{
            background-color: {COLORS['azul_medio']};
            box-shadow: 0 6px 12px rgba(11, 61, 102, 0.3);
            transform: translateY(-1px);
        }}

        /* Botón secundario (ej. Eliminar/Cancelar) en rojo */
        .stButton button[kind="secondary"] {{
            background-color: {COLORS['rojo']};
            box-shadow: 0 4px 6px rgba(215, 38, 61, 0.2);
        }}
        .stButton button[kind="secondary"]:hover {{
            background-color: {COLORS['rojo_hover']};
        }}

        /* Tarjetas de métricas (dashboard) */
        div[data-testid="stMetric"] {{
            background-color: {COLORS['blanco']};
            border-radius: 12px;
            padding: 16px 20px;
            border-left: 5px solid {COLORS['celeste']};
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
            transition: transform 0.2s ease;
        }}
        div[data-testid="stMetric"]:hover {{
            transform: translateY(-2px);
        }}

        /* Tarjetas contenedoras genéricas */
        .transur-card {{
            background-color: {COLORS['blanco']};
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.04);
            margin-bottom: 16px;
            border: 1px solid {COLORS['gris_borde']};
        }}
        
        /* Títulos limpios */
        h1, h2, h3, .transur-title {{
            color: {COLORS['texto_oscuro']};
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
            letter-spacing: -0.5px;
        }}

        /* Alertas rediseñadas */
        .transur-alert-warning {{
            background-color: #FEF2F2;
            color: {COLORS['rojo']};
            border-left: 4px solid {COLORS['rojo']};
            border-radius: 8px;
            padding: 16px;
            font-weight: 500;
            margin-bottom: 16px;
        }}

        /* Inputs: Estilos profesionales y estados de Focus */
        .stTextInput input, .stNumberInput input, .stTextArea textarea {{
            background-color: {COLORS['blanco']} !important;
            color: {COLORS['texto_oscuro']} !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 8px !important;
            padding: 10px 14px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }}
        .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
            border-color: {COLORS['celeste']} !important;
            box-shadow: 0 0 0 3px rgba(41, 171, 226, 0.2) !important;
            outline: none !important;
        }}
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
            color: #9CA3AF !important;
        }}

        /* Selectores desplegables */
        div[data-baseweb="select"] > div {{
            background-color: {COLORS['blanco']} !important;
            color: {COLORS['texto_oscuro']} !important;
            border: 1px solid #D1D5DB !important;
            border-radius: 8px !important;
        }}
        div[data-baseweb="popover"] {{
            background-color: {COLORS['blanco']} !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
        }}
        ul[data-testid="stSelectboxVirtualDropdown"] {{
            background-color: {COLORS['blanco']} !important;
        }}
        ul[data-testid="stSelectboxVirtualDropdown"] li {{
            color: {COLORS['texto_oscuro']} !important;
        }}

        /* Fix para evitar que el fondo gris afecte los textos generales */
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
    """Franja superior rediseñada para ocupar todo el ancho sin márgenes extraños."""
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, {COLORS['azul_profundo']} 0%, {COLORS['azul_medio']} 100%);
            padding: 18px 30px;
            border-radius: 10px;
            margin: -10px 0 24px 0;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 15px rgba(11, 61, 102, 0.15);
        ">
            <div style="display: flex; align-items: baseline; gap: 12px;">
                <span style="color:#FFFFFF; font-size:22px; font-weight:800; letter-spacing: -0.5px;">🚍 Transur 7 de Mayo</span>
                <span style="color: {COLORS['celeste']}; font-size:14px; font-weight:500; border-left: 2px solid rgba(255,255,255,0.2); padding-left: 12px;">{subtitulo}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
