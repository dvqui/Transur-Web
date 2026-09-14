-- =============================================================================
-- BASE DE DATOS: Cooperativa de Transportes "Transur 7 de Mayo"
-- Sistema de Gestión de Repuestos - Version Web
-- Motor: PostgreSQL (compatible con Neon, Supabase, RDS, etc.)
-- =============================================================================

-- -----------------------------------------------------------------------------
-- ROLES DEL SISTEMA
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
    id_rol      SERIAL PRIMARY KEY,
    nombre_rol  VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(200)
);

-- -----------------------------------------------------------------------------
-- USUARIOS (tabla unificada de personas/usuarios: admins, socios y clientes)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario          SERIAL PRIMARY KEY,
    nombres             VARCHAR(100) NOT NULL,
    apellidos           VARCHAR(100) NOT NULL,
    cedula              VARCHAR(20) UNIQUE,
    correo_electronico  VARCHAR(150) NOT NULL UNIQUE,
    telefono            VARCHAR(20),
    direccion           VARCHAR(200),
    nombre_usuario      VARCHAR(50) NOT NULL UNIQUE,
    password_hash       VARCHAR(256) NOT NULL,
    password_salt       VARCHAR(64) NOT NULL,
    id_rol              INTEGER NOT NULL REFERENCES roles(id_rol),
    activo              BOOLEAN NOT NULL DEFAULT TRUE,
    requiere_cambio_pwd BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_registro      TIMESTAMP NOT NULL DEFAULT NOW(),
    ultimo_acceso       TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- BITÁCORA DE RESETEO DE CONTRASEÑAS (auditoría, solo Admin)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reseteos_password (
    id_reseteo      SERIAL PRIMARY KEY,
    id_usuario      INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_admin        INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    fecha_reseteo   TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- CATEGORÍAS Y PROVEEDORES
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre       VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre       VARCHAR(150) NOT NULL,
    contacto     VARCHAR(100),
    telefono     VARCHAR(20),
    correo       VARCHAR(150)
);

-- -----------------------------------------------------------------------------
-- INVENTARIO DE REPUESTOS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS repuestos (
    id_repuesto     SERIAL PRIMARY KEY,
    codigo          VARCHAR(50) NOT NULL UNIQUE,
    nombre          VARCHAR(150) NOT NULL,
    descripcion     VARCHAR(500),
    id_categoria    INTEGER REFERENCES categorias(id_categoria),
    id_proveedor    INTEGER REFERENCES proveedores(id_proveedor),
    precio_compra   NUMERIC(10,2) NOT NULL DEFAULT 0,
    precio_venta    NUMERIC(10,2) NOT NULL DEFAULT 0,
    stock           INTEGER NOT NULL DEFAULT 0,
    stock_minimo    INTEGER NOT NULL DEFAULT 5,
    fecha_registro  TIMESTAMP NOT NULL DEFAULT NOW()
);

-- -----------------------------------------------------------------------------
-- VENTAS Y DETALLE DE VENTAS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ventas (
    id_venta        SERIAL PRIMARY KEY,
    id_cliente      INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_vendedor     INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    fecha_venta     TIMESTAMP NOT NULL DEFAULT NOW(),
    total           NUMERIC(10,2) NOT NULL DEFAULT 0,
    estado          VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE'
);

CREATE TABLE IF NOT EXISTS detalle_ventas (
    id_detalle      SERIAL PRIMARY KEY,
    id_venta        INTEGER NOT NULL REFERENCES ventas(id_venta) ON DELETE CASCADE,
    id_repuesto     INTEGER NOT NULL REFERENCES repuestos(id_repuesto),
    cantidad        INTEGER NOT NULL,
    precio_unitario NUMERIC(10,2) NOT NULL,
    subtotal        NUMERIC(10,2) NOT NULL
);

-- -----------------------------------------------------------------------------
-- PAGOS
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS pagos (
    id_pago       SERIAL PRIMARY KEY,
    id_venta      INTEGER NOT NULL REFERENCES ventas(id_venta),
    monto         NUMERIC(10,2) NOT NULL,
    fecha_pago    TIMESTAMP NOT NULL DEFAULT NOW(),
    metodo_pago   VARCHAR(30) NOT NULL DEFAULT 'EFECTIVO',
    referencia    VARCHAR(100)
);

-- -----------------------------------------------------------------------------
-- ÍNDICES
-- -----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_repuestos_nombre ON repuestos(nombre);
CREATE INDEX IF NOT EXISTS idx_usuarios_rol ON usuarios(id_rol);
CREATE INDEX IF NOT EXISTS idx_ventas_cliente ON ventas(id_cliente);
CREATE INDEX IF NOT EXISTS idx_detalle_venta ON detalle_ventas(id_venta);
