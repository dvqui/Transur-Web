"""Validadores reutilizables para formularios del sistema."""
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validar_email(correo: str) -> bool:
    if not correo:
        return False
    return bool(EMAIL_REGEX.match(correo.strip()))


def validar_no_vacio(valor: str) -> bool:
    return bool(valor and valor.strip())


def validar_numero_positivo(valor) -> bool:
    try:
        return float(valor) >= 0
    except (TypeError, ValueError):
        return False


def validar_entero_positivo(valor) -> bool:
    try:
        return int(valor) >= 0
    except (TypeError, ValueError):
        return False


def validar_password_segura(password: str) -> tuple[bool, str]:
    """Valida longitud mínima. Devuelve (es_valida, mensaje_error)."""
    if not password or len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    return True, ""
