# Aplicación web para Consulta y Compartición Segura del Estado VIH

## Descripción

Este proyecto es una aplicación web desarrollada con Flask que permite a usuarios consultar y compartir su estado VIH de manera segura mediante tokens dinámicos. Los usuarios pueden registrarse, iniciar sesión, ver detalles ampliados de su estado de salud y generar un token temporal para compartir su información con terceros sin comprometer su privacidad. Además, cualquier persona puede consultar el estado VIH de un usuario ingresando un token válido sin necesidad de iniciar sesión.

---

## Funcionalidades Principales

- Registro y autenticación de usuarios.
- Visualización detallada del estado VIH incluyendo:
  - Estado general (positivo, negativo, etc.).
  - Fecha de última prueba.
  - Resultado de carga viral.
  - Conteo actual de CD4.
  - Tratamiento actual.
  - Control médico.
- Generación de tokens dinámicos para compartir el estado VIH de forma segura.
- Consulta pública de estado VIH mediante ingreso de token, sin necesidad de autenticación.
- Interfaz sencilla y amigable.

---

## Tecnologías

- **Backend:** Python 3.x, Flask
- **Base de datos:** SQLite
- **Autenticación:** Session Flask
- **Seguridad:** Hash de contraseñas con `werkzeug.security`
- **Tokens:** JSON Web Tokens (JWT) para generación y validación dinámica

---

## Estructura del Proyecto

- `app.py`: Archivo principal con rutas y lógica Flask.
- `models.py`: Funciones para manipulación de base de datos SQLite.
- `utils.py`: Funciones para generación y validación de tokens dinámicos.
- `templates/`: Carpeta con archivos HTML para vistas.
- `db.sqlite3`: Base de datos SQLite con la tabla `users`.
- `README.md`: Documentación del proyecto.

---
