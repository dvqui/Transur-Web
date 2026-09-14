"""Servicio de gestión de pagos asociados a ventas."""
from database.connection import ejecutar, consultar, consultar_uno


class PagoServiceError(Exception):
    pass


class PagoService:
    def registrar_pago(self, id_venta: int, monto: float, metodo_pago: str, referencia: str = ""):
        venta = consultar_uno("SELECT * FROM ventas WHERE id_venta = %s", (id_venta,))
        if venta is None:
            raise PagoServiceError("La venta seleccionada no existe.")

        total_pagado = float(
            consultar_uno(
                "SELECT COALESCE(SUM(monto), 0) AS total FROM pagos WHERE id_venta = %s", (id_venta,)
            )["total"]
        )

        if total_pagado + monto > float(venta["total"]) + 0.01:
            raise PagoServiceError("El monto excede el saldo pendiente de la venta.")

        ejecutar(
            "INSERT INTO pagos (id_venta, monto, metodo_pago, referencia) VALUES (%s, %s, %s, %s)",
            (id_venta, monto, metodo_pago, referencia or None),
        )

        nuevo_total_pagado = total_pagado + monto
        if nuevo_total_pagado >= float(venta["total"]) - 0.01:
            ejecutar("UPDATE ventas SET estado = 'PAGADA' WHERE id_venta = %s", (id_venta,))

    def listar_pagos(self, filtro: str = ""):
        patron = f"%{filtro}%"
        return consultar(
            """
            SELECT p.id_pago, p.fecha_pago, p.monto, p.metodo_pago, p.referencia,
                   v.id_venta, (c.nombres || ' ' || c.apellidos) AS cliente
            FROM pagos p
            JOIN ventas v ON v.id_venta = p.id_venta
            JOIN usuarios c ON c.id_usuario = v.id_cliente
            WHERE c.nombres ILIKE %s OR c.apellidos ILIKE %s OR p.metodo_pago ILIKE %s
            ORDER BY p.id_pago DESC
            """,
            (patron, patron, patron),
        )

    def saldo_pendiente(self, id_venta: int) -> float:
        venta = consultar_uno("SELECT total FROM ventas WHERE id_venta = %s", (id_venta,))
        pagado = consultar_uno(
            "SELECT COALESCE(SUM(monto),0) AS total FROM pagos WHERE id_venta = %s", (id_venta,)
        )["total"]
        return float(venta["total"] if venta else 0) - float(pagado)
