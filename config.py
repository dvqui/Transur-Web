"""Configuración global de la aplicación web - Transur 7 de Mayo."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

APP_NAME = "Transur 7 de Mayo - Gestión de Repuestos"
APP_VERSION = "3.0-web"

COLORS = {
    "azul_profundo": "#0B3D66",
    "azul_oscuro": "#082C4B",
    "azul_medio": "#124E82",
    "celeste": "#29ABE2",
    "rojo": "#D7263D",
    "rojo_hover": "#B01E30",
    "blanco": "#FFFFFF",
    "gris_fondo": "#F3F6F9",
    "gris_borde": "#E2E8F0",
    "gris_texto": "#5A6B7B",
    "texto_oscuro": "#1B2A38",
    "verde_exito": "#1E8E5A",
    "amarillo_aviso": "#E8A427",
}

ROLE_ADMIN = "Administrador"
ROLE_SOCIO = "Socio"
ROLE_CLIENTE = "Cliente Externo"
ROLES = [ROLE_ADMIN, ROLE_SOCIO, ROLE_CLIENTE]

DEFAULT_STOCK_MINIMO = 5
