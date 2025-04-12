# NewsScraper ETL System

Este proyecto implementa un sistema completo de Extracción, Transformación y Carga (ETL) para noticias, utilizando **Scrapy**, **PostgreSQL**, una **arquitectura de lago de datos** y visualización con **Streamlit**.

---

## Objetivos del Proyecto

- Extraer automáticamente artículos desde varias fuentes web.
- Validar y transformar datos con Scrapy Items y Pipelines.
- Almacenar datos en formatos estructurados: JSONL, CSV y PostgreSQL.
- Organizar los datos bajo una arquitectura de Data Lake.
- Visualizar estadísticas clave en un panel interactivo con filtros dinámicos.
- Enriquecer los datos con una API externa (clima actual de una ciudad).

---

## Tecnologías y Librerías Usadas

- **Python 3.10+**
- **Scrapy**: motor de web scraping.
- **PostgreSQL**: base de datos relacional para datos validados.
- **psycopg2**: conector Python ↔ PostgreSQL.
- **Streamlit**: biblioteca para visualización de datos.
- **Requests**: para consumir API externa (OpenWeatherMap).
- **Datetime, Email.utils**: para manejo y transformación de fechas.
- **JSON / CSV / JSONL**: para formatos de almacenamiento plano.

---

## Instalación

Instala las dependencias necesarias:

```bash
pip install scrapy psycopg2-binary streamlit requests
```

### Configura PostgreSQL

1. Crea la base de datos `scraping_db`.
2. Crea la tabla `articles` con la siguiente estructura:

```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT,
    url TEXT UNIQUE,
    date DATE,
    source TEXT,
    summary TEXT
);
```

---

## Ejecución del Scraper

Desde la raíz del proyecto, puedes ejecutar:

```bash
scrapy crawl quotes
scrapy crawl npr
scrapy crawl aljazeera
scrapy crawl nyt
```

### Alternativa automática:

Haz doble click en:  
```bash
ejecutar_scrapers.bat
```

---

## Limpieza y Validación

### Validación (conteo de artículos únicos):
```bash
cd output
python contar_articulos.py
```

### Limpiar base de datos PostgreSQL:
```bash
python limpiar_postgres.py
```

---

## Exportar a CSV desde PostgreSQL

```bash
python exportar_postgres_csv.py
```

El archivo generado se llama `articles_postgres.csv` y contiene los datos procesados.

---

El pipeline implementado incluye:

- Normalización de texto (strip, replace).
- Conversión de fechas a formato ISO (`YYYY-MM-DD`).
- Validación de unicidad (campo `url` con `ON CONFLICT DO NOTHING`).
- Exportación en paralelo a:
  - `output/articles_final.jsonl`
  - `scraping_db.articles`

---


## Arquitectura del Lago de Datos

```
datalake/
├── LANDING_ZONE/         # Datos crudos (.jsonl)
├── REFINED_ZONE/         # Datos limpios exportados de PostgreSQL (.csv)
└── CONSUMPTION_ZONE/     # Datos agregados listos para análisis (.csv)
```

---

## Visualización con Streamlit


```bash
cd dashboard
streamlit run dashboard.py
```

Configuración con variables de entorno `.env`:

```env
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=Root123$$
DB_DATABASE=scraping_db
```

---

### Funcionalidades del Panel

- Filtro por fecha (`st.date_input()`).
- Métrica total de artículos (`st.metric()`).
- Gráfico de barras (`st.bar_chart()`).
- Tabla con conteo por fuente (`st.dataframe()`).
- API externa OpenWeatherMap integrada:
  - Se consulta clima por ciudad ingresada.
  - Muestra temperatura, clima y humedad.

---

## Estructura del proyecto

news_scraper/
├── news_scraper/
│   ├── spiders/
│   ├── pipelines/
│   │   ├── landing_news_pipeline.py
│   │   ├── refined_news_pipeline.py
│   │   └── consumption_news_pipeline.py
│   ├── items.py
│   └── settings.py
├── datalake/
│   ├── LANDING_ZONE/
│   ├── REFINED_ZONE/
│   └── CONSUMPTION_ZONE/
├── dashboard/
│   └── dashboard.py
├── ejecutar_scrapers.bat
├── requirements.txt
├── README.md
└── informe_final.pdf
```

---

## Scripts Incluidos

- `exportar_postgres_csv.py`: exporta datos limpios a CSV.
- `exportar_resumen.py`: genera resumen por fuente.
- `contar_articulos.py`: cuenta artículos únicos.
- `limpiar_postgres.py`: borra registros en PostgreSQL.

---

## Buenas Prácticas Aplicadas

- Uso de `USER_AGENT` personalizado.
- Respeto a `robots.txt` (`ROBOTSTXT_OBEY = True`).
- `DOWNLOAD_DELAY = 2` para evitar bloqueo.
- `AUTOTHROTTLE` habilitado.
- Codificación UTF-8 garantizada.

---

## Notas finales

- El archivo `.jsonl` contiene los artículos únicos procesados.
- Los datos en PostgreSQL pueden ser consultados o exportados.
- Se incluye scripts auxiliares para limpiar,validar y exportar los datos.

## Licencia

Yamil Gamarra López - Abril 2025.



