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

        /* Botones principales */
        .stButton button, .stDownloadButton button {{
            background-color: {COLORS['azul_profundo']};
            color: white;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }}
        .stButton button:hover, .stDownloadButton button:hover {{
            background-color: {COLORS['azul_oscuro']};
            color: white;
        }}

        /* Tarjetas de estadísticas (dashboard) */
        div[data-testid="stMetric"] {{
            background-color: {COLORS['blanco']};
            border-radius: 14px;
            padding: 16px 18px;
            border-left: 6px solid {COLORS['azul_profundo']};
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        }}

        /* Tarjetas contenedoras genéricas */
        .transur-card {{
            background-color: {COLORS['blanco']};
            border-radius: 14px;
            padding: 20px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            margin-bottom: 14px;
        }}
        .transur-title {{
            color: {COLORS['texto_oscuro']};
            font-weight: 700;
        }}
        .transur-alert-warning {{
            background-color: #FDECEC;
            color: {COLORS['rojo']};
            border-radius: 10px;
            padding: 14px 18px;
            font-weight: 600;
            margin-bottom: 16px;
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            font-weight: 600;
        }}

        /* Inputs */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
