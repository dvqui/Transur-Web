"""Servicio de ventas: registro con detalle multi-ítem y control de stock."""
from database.connection import ejecutar, ejecutar_retornando, consultar, consultar_uno


class VentaServiceError(Exception):
    pass


class VentaService:
    def crear_venta(self, id_cliente: int, id_vendedor: int, items: list):
        if not items:
            raise VentaServiceError("La venta debe contener al menos un repuesto.")

        for item in items:
            rep = consultar_uno(
                "SELECT stock, nombre FROM repuestos WHERE id_repuesto = %s", (item["id_repuesto"],)
            )
            if rep is None:
                raise VentaServiceError("Uno de los repuestos seleccionados no existe.")
            if rep["stock"] < item["cantidad"]:
                raise VentaServiceError(
                    f"Stock insuficiente para '{rep['nombre']}'. Disponible: {rep['stock']}."
                )

        total = sum(i["cantidad"] * i["precio_unitario"] for i in items)

        row = ejecutar_retornando(
            "INSERT INTO ventas (id_cliente, id_vendedor, total, estado) "
            "VALUES (%s, %s, %s, 'PENDIENTE') RETURNING id_venta",
            (id_cliente, id_vendedor, total),
        )
        id_venta = row["id_venta"]

        for item in items:
            subtotal = item["cantidad"] * item["precio_unitario"]
            ejecutar(
                """INSERT INTO detalle_ventas
                   (id_venta, id_repuesto, cantidad, precio_unitario, subtotal)
                   VALUES (%s, %s, %s, %s, %s)""",
                (id_venta, item["id_repuesto"], item["cantidad"], item["precio_unitario"], subtotal),
            )
            ejecutar(
                "UPDATE repuestos SET stock = stock - %s WHERE id_repuesto = %s",
                (item["cantidad"], item["id_repuesto"]),
            )
        return id_venta

    def listar_ventas(self, filtro: str = ""):
        patron = f"%{filtro}%"
        return consultar(
            """
            SELECT v.id_venta, v.fecha_venta, v.total, v.estado,
                   (c.nombres || ' ' || c.apellidos) AS cliente,
                   (ve.nombres || ' ' || ve.apellidos) AS vendedor
            FROM ventas v
            JOIN usuarios c ON c.id_usuario = v.id_cliente
            JOIN usuarios ve ON ve.id_usuario = v.id_vendedor
            WHERE c.nombres ILIKE %s OR c.apellidos ILIKE %s OR v.estado ILIKE %s
            ORDER BY v.id_venta DESC
            """,
            (patron, patron, patron),
        )

    def detalle_venta(self, id_venta: int):
        return consultar(
            """
            SELECT d.*, r.nombre AS nombre_repuesto, r.codigo
            FROM detalle_ventas d JOIN repuestos r ON r.id_repuesto = d.id_repuesto
            WHERE d.id_venta = %s
            """,
            (id_venta,),
        )

    def actualizar_estado(self, id_venta: int, estado: str):
        ejecutar("UPDATE ventas SET estado = %s WHERE id_venta = %s", (estado, id_venta))

    def clientes_y_socios(self):
        return consultar(
            """
            SELECT u.id_usuario, (u.nombres || ' ' || u.apellidos) AS nombre_completo, r.nombre_rol
            FROM usuarios u JOIN roles r ON r.id_rol = u.id_rol
            WHERE r.nombre_rol IN ('Socio', 'Cliente Externo') AND u.activo = TRUE
            ORDER BY u.nombres
            """
        )
