"""Servicio CRUD de usuarios (Administradores, Socios y Clientes Externos)."""
from database.connection import ejecutar, ejecutar_retornando, consultar, consultar_uno
from utils.security import generar_salt, hash_password
from utils.validators import validar_email


class UsuarioServiceError(Exception):
    pass


class UsuarioService:
    def crear_usuario(
        self, nombres, apellidos, cedula, correo_electronico, telefono, direccion,
        nombre_usuario, password, nombre_rol,
    ) -> int:
        if not validar_email(correo_electronico):
            raise UsuarioServiceError("El formato del correo electrónico no es válido.")

        existe = consultar_uno(
            "SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s OR correo_electronico = %s",
            (nombre_usuario, correo_electronico),
        )
        if existe:
            raise UsuarioServiceError("Ya existe un usuario con ese nombre de usuario o correo.")

        rol = consultar_uno("SELECT id_rol FROM roles WHERE nombre_rol = %s", (nombre_rol,))
        if rol is None:
            raise UsuarioServiceError("El rol seleccionado no existe.")

        salt = generar_salt()
        password_hash = hash_password(password, salt)

        row = ejecutar_retornando(
            """
            INSERT INTO usuarios
                (nombres, apellidos, cedula, correo_electronico, telefono, direccion,
                 nombre_usuario, password_hash, password_salt, id_rol, activo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            RETURNING id_usuario
            """,
            (nombres, apellidos, cedula or None, correo_electronico, telefono, direccion,
             nombre_usuario, password_hash, salt, rol["id_rol"]),
        )
        return row["id_usuario"]

    def listar_usuarios(self, filtro: str = "", rol: str = None):
        query = """
            SELECT u.id_usuario, u.nombres, u.apellidos, u.cedula, u.correo_electronico,
                   u.telefono, u.direccion, u.nombre_usuario, u.activo, r.nombre_rol,
                   u.fecha_registro, u.ultimo_acceso
            FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol
            WHERE (u.nombres ILIKE %s OR u.apellidos ILIKE %s OR u.correo_electronico ILIKE %s
                   OR u.nombre_usuario ILIKE %s OR COALESCE(u.cedula,'') ILIKE %s)
        """
        patron = f"%{filtro}%"
        params = [patron] * 5
        if rol:
            query += " AND r.nombre_rol = %s"
            params.append(rol)
        query += " ORDER BY u.id_usuario DESC"
        return consultar(query, tuple(params))

    def obtener_usuario(self, id_usuario: int):
        return consultar_uno(
            """
            SELECT u.*, r.nombre_rol FROM usuarios u
            JOIN roles r ON r.id_rol = u.id_rol WHERE u.id_usuario = %s
            """,
            (id_usuario,),
        )

    def listar_roles(self):
        return consultar("SELECT * FROM roles ORDER BY id_rol")

    def actualizar_usuario(
        self, id_usuario, nombres, apellidos, cedula, correo_electronico, telefono,
        direccion, nombre_rol,
    ):
        if not validar_email(correo_electronico):
            raise UsuarioServiceError("El formato del correo electrónico no es válido.")

        duplicado = consultar_uno(
            "SELECT id_usuario FROM usuarios WHERE correo_electronico = %s AND id_usuario != %s",
            (correo_electronico, id_usuario),
        )
        if duplicado:
            raise UsuarioServiceError("Ese correo ya está registrado por otro usuario.")

        rol = consultar_uno("SELECT id_rol FROM roles WHERE nombre_rol = %s", (nombre_rol,))
        if rol is None:
            raise UsuarioServiceError("El rol seleccionado no existe.")

        ejecutar(
            """
            UPDATE usuarios
            SET nombres = %s, apellidos = %s, cedula = %s, correo_electronico = %s,
                telefono = %s, direccion = %s, id_rol = %s
            WHERE id_usuario = %s
            """,
            (nombres, apellidos, cedula or None, correo_electronico, telefono, direccion,
             rol["id_rol"], id_usuario),
        )

    def cambiar_estado(self, id_usuario: int, activo: bool):
        ejecutar("UPDATE usuarios SET activo = %s WHERE id_usuario = %s", (activo, id_usuario))

    def eliminar_usuario(self, id_usuario: int):
        # Se deshabilita en lugar de borrar físicamente, para preservar el
        # historial de ventas/pagos asociado (integridad referencial).
        self.cambiar_estado(id_usuario, False)
