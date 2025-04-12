import os

# Ruta donde crearás la carpeta del dashboard
dashboard_path = "dashboard"
streamlit_config_path = os.path.join(dashboard_path, ".streamlit")
os.makedirs(streamlit_config_path, exist_ok=True)

# Archivos que se crearán con contenido básico
archivos_dashboard = {
    ".env": """DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=Root123$$
DB_DATABASE=scraping_db
""",
    "secrets.toml": """[general]
email = "tucorreo@ejemplo.com"
""",
    "__init__.py": "# Este archivo hace que 'dashboard' sea un módulo de Python",
    "dashboard.py": "# Aquí pegarás tu código completo de viz.py",
    ".streamlit/config.toml": """[theme]
base="dark"

[server]
headless=true
port=8501
"""
}

# Crear los archivos
for ruta, contenido in archivos_dashboard.items():
    full_path = os.path.join(dashboard_path, ruta)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(contenido)

print("✅ Estructura 'dashboard/' generada correctamente.")

