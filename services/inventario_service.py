"""Servicio CRUD de inventario de repuestos, categorías y proveedores."""
from database.connection import ejecutar, ejecutar_retornando, consultar, consultar_uno


class InventarioServiceError(Exception):
    pass


class InventarioService:
    def crear_repuesto(
        self, codigo, nombre, descripcion, id_categoria, id_proveedor,
        precio_compra, precio_venta, stock, stock_minimo,
    ):
        existe = consultar_uno("SELECT id_repuesto FROM repuestos WHERE codigo = %s", (codigo,))
        if existe:
            raise InventarioServiceError(f"Ya existe un repuesto con el código '{codigo}'.")

        row = ejecutar_retornando(
            """
            INSERT INTO repuestos
                (codigo, nombre, descripcion, id_categoria, id_proveedor,
                 precio_compra, precio_venta, stock, stock_minimo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_repuesto
            """,
            (codigo, nombre, descripcion, id_categoria, id_proveedor,
             precio_compra, precio_venta, stock, stock_minimo),
        )
        return row["id_repuesto"]

    def listar_repuestos(self, filtro: str = ""):
        patron = f"%{filtro}%"
        return consultar(
            """
            SELECT r.*, c.nombre AS nombre_categoria, p.nombre AS nombre_proveedor
            FROM repuestos r
            LEFT JOIN categorias c ON c.id_categoria = r.id_categoria
            LEFT JOIN proveedores p ON p.id_proveedor = r.id_proveedor
            WHERE r.nombre ILIKE %s OR r.codigo ILIKE %s
            ORDER BY r.id_repuesto DESC
            """,
            (patron, patron),
        )

    def obtener_repuesto(self, id_repuesto: int):
        return consultar_uno("SELECT * FROM repuestos WHERE id_repuesto = %s", (id_repuesto,))

    def actualizar_repuesto(
        self, id_repuesto, codigo, nombre, descripcion, id_categoria, id_proveedor,
        precio_compra, precio_venta, stock, stock_minimo,
    ):
        duplicado = consultar_uno(
            "SELECT id_repuesto FROM repuestos WHERE codigo = %s AND id_repuesto != %s",
            (codigo, id_repuesto),
        )
        if duplicado:
            raise InventarioServiceError(f"El código '{codigo}' ya pertenece a otro repuesto.")

        ejecutar(
            """
            UPDATE repuestos
            SET codigo = %s, nombre = %s, descripcion = %s, id_categoria = %s, id_proveedor = %s,
                precio_compra = %s, precio_venta = %s, stock = %s, stock_minimo = %s
            WHERE id_repuesto = %s
            """,
            (codigo, nombre, descripcion, id_categoria, id_proveedor,
             precio_compra, precio_venta, stock, stock_minimo, id_repuesto),
        )

    def eliminar_repuesto(self, id_repuesto: int):
        ejecutar("DELETE FROM repuestos WHERE id_repuesto = %s", (id_repuesto,))

    def repuestos_bajo_stock(self):
        return consultar("SELECT * FROM repuestos WHERE stock <= stock_minimo ORDER BY stock ASC")

    def listar_categorias(self):
        return consultar("SELECT * FROM categorias ORDER BY nombre")

    def crear_categoria(self, nombre):
        ejecutar("INSERT INTO categorias (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING", (nombre,))

    def listar_proveedores(self):
        return consultar("SELECT * FROM proveedores ORDER BY nombre")

    def crear_proveedor(self, nombre, contacto, telefono, correo):
        row = ejecutar_retornando(
            "INSERT INTO proveedores (nombre, contacto, telefono, correo) VALUES (%s, %s, %s, %s) "
            "RETURNING id_proveedor",
            (nombre, contacto, telefono, correo),
        )
        return row["id_proveedor"]
