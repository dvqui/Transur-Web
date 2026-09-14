"""Servicio de autenticación y gestión de contraseñas (PostgreSQL)."""
from database.connection import ejecutar, consultar_uno
from utils.security import (
    generar_salt, hash_password, verificar_password, generar_password_temporal,
)


class AuthError(Exception):
    pass


class AuthService:
    def login(self, nombre_usuario: str, password: str) -> dict:
        row = consultar_uno(
            """
            SELECT u.*, r.nombre_rol
            FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol
            WHERE u.nombre_usuario = %s
            """,
            (nombre_usuario,),
        )
        if row is None:
            raise AuthError("Usuario o contraseña incorrectos.")
        if not row["activo"]:
            raise AuthError("Este usuario se encuentra deshabilitado. Contacte al administrador.")
        if not verificar_password(password, row["password_salt"], row["password_hash"]):
            raise AuthError("Usuario o contraseña incorrectos.")

        ejecutar(
            "UPDATE usuarios SET ultimo_acceso = NOW() WHERE id_usuario = %s",
            (row["id_usuario"],),
        )

        return {
            "id_usuario": row["id_usuario"],
            "nombres": row["nombres"],
            "apellidos": row["apellidos"],
            "correo_electronico": row["correo_electronico"],
            "nombre_usuario": row["nombre_usuario"],
            "rol": row["nombre_rol"],
            "requiere_cambio_pwd": bool(row["requiere_cambio_pwd"]),
        }

    def cambiar_password(self, id_usuario: int, password_actual: str, password_nueva: str):
        row = consultar_uno(
            "SELECT password_hash, password_salt FROM usuarios WHERE id_usuario = %s",
            (id_usuario,),
        )
        if row is None or not verificar_password(password_actual, row["password_salt"], row["password_hash"]):
            raise AuthError("La contraseña actual no es correcta.")

        nuevo_salt = generar_salt()
        nuevo_hash = hash_password(password_nueva, nuevo_salt)
        ejecutar(
            """UPDATE usuarios SET password_hash = %s, password_salt = %s,
               requiere_cambio_pwd = FALSE WHERE id_usuario = %s""",
            (nuevo_hash, nuevo_salt, id_usuario),
        )

    def resetear_password_admin(self, id_usuario: int, id_admin: int) -> str:
        """Solo el Administrador puede ejecutar esto (validado en la capa de UI)."""
        temp_password = generar_password_temporal()
        nuevo_salt = generar_salt()
        nuevo_hash = hash_password(temp_password, nuevo_salt)

        ejecutar(
            """UPDATE usuarios SET password_hash = %s, password_salt = %s,
               requiere_cambio_pwd = TRUE WHERE id_usuario = %s""",
            (nuevo_hash, nuevo_salt, id_usuario),
        )
        ejecutar(
            "INSERT INTO reseteos_password (id_usuario, id_admin) VALUES (%s, %s)",
            (id_usuario, id_admin),
        )
        return temp_password
