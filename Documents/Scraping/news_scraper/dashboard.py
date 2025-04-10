import streamlit as st
import pandas as pd
import psycopg2
import requests
from datetime import date

# CONFIGURACIÓN INICIAL
st.set_page_config(page_title="📰 Dashboard de Noticias", layout="wide")

API_KEY = "067795edcbb0238a38685c19948cf81d"  # Reemplaza con tu clave real

# 🔌 Conexión a PostgreSQL
@st.cache_data
def cargar_datos(fecha):
    conn = psycopg2.connect(
        host="localhost",
        database="scraping_db",
        user="postgres",
        password="Root123$$"
    )
    query = f"""
        SELECT source, COUNT(*) as total_articles
        FROM articles
        WHERE date >= '{fecha}'
        GROUP BY source;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

@st.cache_data
def total_articulos():
    conn = psycopg2.connect(
        host="localhost",
        database="scraping_db",
        user="postgres",
        password="Root123$$"
    )
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM articles")
    total = cur.fetchone()[0]
    conn.close()
    return total

def obtener_clima(ciudad):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric&lang=es"
    try:
        r = requests.get(url)
        d = r.json()
        if r.status_code == 200:
            return {
                "Ciudad": ciudad.title(),
                "Temperatura (°C)": d["main"]["temp"],
                "Clima": d["weather"][0]["description"],
                "Humedad (%)": d["main"]["humidity"]
            }
        else:
            return {"Error": d.get("message", "Error")}
    except:
        return {"Error": "No se pudo conectar"}

# 🎯 Título principal y stats
st.title("📰 Dashboard de Noticias Scrapeadas")
st.markdown("### Total de artículos recolectados desde todas las fuentes")

col1, col2 = st.columns([1, 3])
with col1:
    st.metric("Total Scraped", total_articulos())

# 📆 Filtro por fecha
fecha = st.date_input("Filtrar artículos desde:", value=date.today(), min_value=date(2024, 1, 1))
df = cargar_datos(fecha)

# 🔢 Tabla y gráfico
st.markdown("### Estadísticas por fuente de noticias")
colA, colB = st.columns(2)
with colA:
    st.dataframe(df)
with colB:
    st.bar_chart(df.set_index("source"))

# 🌦️ API externa: clima
st.markdown("### Consulta el clima actual")
ciudad = st.text_input("Ciudad:", value="New York")
if ciudad:
    clima = obtener_clima(ciudad)
    st.write(clima)

