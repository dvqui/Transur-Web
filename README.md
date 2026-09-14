# Transur 7 de Mayo — Sistema de Gestión de Repuestos (versión Web)

App web construida con **Streamlit** (Python) y **PostgreSQL** (pensada para
**Neon**, base de datos serverless gratuita). Mantiene la misma paleta de
colores, logo, roles, CRUD y exportación a Excel de la versión de escritorio.

Este documento te lleva paso a paso: **Neon → GitHub → Streamlit Community
Cloud**, todo gratis.

---

## PASO 1 — Crear la base de datos en Neon (gratis)

1. Ve a **https://neon.tech** y crea una cuenta gratuita (puedes usar tu
   cuenta de GitHub para registrarte más rápido).
2. Crea un nuevo **Proyecto** (por ejemplo `transur-repuestos`).
3. Neon te dará automáticamente una base de datos y una **cadena de
   conexión** (Connection String). Se ve así:
   ```
   postgresql://usuario:password@ep-xxxxx-xxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. Cópiala y guárdala — la necesitarás en el Paso 3. **No la compartas
   públicamente ni la subas a GitHub.**

> No necesitas ejecutar tú mismo las sentencias SQL: la app crea las tablas
> automáticamente la primera vez que arranca (ver `database/schema_postgres.sql`
> si quieres revisarlas o ejecutarlas manualmente desde el editor SQL de Neon).

---

## PASO 2 — Subir el proyecto a GitHub

1. Ve a **https://github.com** y crea un repositorio nuevo, por ejemplo
   `transur-repuestos-web` (puede ser público o privado).
2. Descomprime este ZIP en tu computador y, dentro de esa carpeta, ejecuta:
   ```bash
   git init
   git add .
   git commit -m "Version inicial - Transur 7 de Mayo web"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/transur-repuestos-web.git
   git push -u origin main
   ```
3. **Verifica que `.streamlit/secrets.toml` NO se haya subido** (el
   `.gitignore` ya lo excluye). Solo debe subirse `secrets.toml.example`.

---

## PASO 3 — Desplegar en Streamlit Community Cloud (gratis)

1. Ve a **https://share.streamlit.io** e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New app"**.
3. Selecciona tu repositorio `transur-repuestos-web`, la rama `main`, y como
   **Main file path** escribe: `app.py`.
4. Antes de darle a "Deploy", entra a **"Advanced settings" → "Secrets"** y
   pega lo siguiente (reemplazando con tu cadena real de Neon):
   ```toml
   DATABASE_URL = "postgresql://usuario:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require"
   ```
5. Haz clic en **"Deploy"**. En 1–2 minutos tu app estará en línea en una URL
   como `https://transur-repuestos-web.streamlit.app`.

Cuando quieras actualizar el sistema, solo haz `git push` de tus cambios:
Streamlit Cloud vuelve a desplegar automáticamente.

---

## Acceso por defecto

```
Usuario:    admin
Contraseña: admin123
```

⚠️ Cámbiala apenas entres (botón "🔑 Cambiar contraseña" en el menú lateral).

---

## Estructura del proyecto

```
transur_web/
├── app.py                       # Punto de entrada: login, sesión, navegación
├── config.py                     # Colores institucionales y constantes
├── requirements.txt
├── .streamlit/
│   ├── config.toml                # Tema visual (colores) de Streamlit
│   └── secrets.toml.example       # Plantilla — copiar como secrets.toml en local
├── database/
│   ├── schema_postgres.sql         # Sentencias SQL (PostgreSQL / Neon)
│   └── connection.py                # Conexión + creación de esquema/datos base
├── services/                      # Lógica de negocio (idéntica a la versión desktop)
│   ├── auth_service.py
│   ├── usuario_service.py
│   ├── inventario_service.py
│   ├── venta_service.py
│   ├── pago_service.py
│   └── export_service.py            # Genera el Excel en memoria (BytesIO)
├── pages_ui/                      # Interfaz (páginas Streamlit)
│   ├── estilos.py                    # CSS institucional
│   ├── componentes.py                # Paginación reutilizable
│   ├── dashboard.py
│   ├── inventario.py
│   ├── usuarios.py
│   ├── ventas.py
│   ├── pagos.py
│   └── reportes.py
├── utils/
│   ├── security.py                   # Hash de contraseñas (PBKDF2-HMAC-SHA256)
│   └── validators.py                 # Validación de correo, etc.
└── assets/
    └── logo.png                       # Logo (placeholder, reemplázalo por el oficial)
```

## Ejecutarlo en tu computador (antes de subirlo)

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt

# Copia la plantilla de secretos y pon tu cadena de conexión real de Neon:
copy .streamlit\secrets.toml.example .streamlit\secrets.toml    # Windows
# cp .streamlit/secrets.toml.example .streamlit/secrets.toml    # Linux/Mac

streamlit run app.py
```

Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

## Roles del sistema

| Rol                | Permisos |
|---------------------|-----------|
| **Administrador**   | Acceso total: usuarios, inventario, ventas, pagos, reportes, resetear contraseñas |
| **Socio**           | Dashboard, inventario, ventas, pagos |
| **Cliente Externo** | Igual que Socio |

Los módulos **Usuarios y Socios** y **Reportes Excel** solo aparecen si el
usuario conectado tiene rol `Administrador`.

## Seguridad

- Contraseñas con **PBKDF2-HMAC-SHA256** (200,000 iteraciones) + salt único
  por usuario — nunca se guardan en texto plano.
- Solo el Administrador puede restablecer la contraseña de otro usuario;
  queda registrado en la tabla `reseteos_password` (quién, a quién, cuándo).
- `DATABASE_URL` vive solo en "Secrets" de Streamlit Cloud (o en tu
  `secrets.toml` local, que nunca se sube a GitHub).

## Notas sobre el plan gratuito de Neon

El plan gratuito de Neon "suspende" la base de datos tras un periodo de
inactividad y la reactiva automáticamente en la primera consulta (puede
tardar unos segundos la primera carga tras la inactividad). Esto es normal
y no afecta tus datos, que permanecen guardados.
