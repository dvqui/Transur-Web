"""
Utilidades de seguridad: hashing y verificación de contraseñas.
Se usa PBKDF2-HMAC-SHA256 (librería estándar 'hashlib'), 200,000 iteraciones,
con un salt aleatorio distinto por usuario. No se requieren dependencias
externas de compilación (evita problemas de instalación de 'bcrypt' en
entornos sin compilador).
"""
import hashlib
import os
import secrets
import string

_ITERATIONS = 200_000
_ALGO = "sha256"


def generar_salt() -> str:
    """Genera un salt aleatorio criptográficamente seguro."""
    return secrets.token_hex(16)


def hash_password(password: str, salt: str) -> str:
    """Devuelve el hash PBKDF2-HMAC-SHA256 de una contraseña + salt."""
    dk = hashlib.pbkdf2_hmac(
        _ALGO, password.encode("utf-8"), salt.encode("utf-8"), _ITERATIONS
    )
    return dk.hex()


def verificar_password(password: str, salt: str, hash_guardado: str) -> bool:
    """Compara de forma segura la contraseña ingresada contra el hash guardado."""
    hash_calculado = hash_password(password, salt)
    return secrets.compare_digest(hash_calculado, hash_guardado)


def generar_password_temporal(longitud: int = 10) -> str:
    """Genera una contraseña temporal segura (usada por el Administrador
    al restablecer la clave de un usuario)."""
    alfabeto = string.ascii_letters + string.digits + "!@#$%"
    return "".join(secrets.choice(alfabeto) for _ in range(longitud))
