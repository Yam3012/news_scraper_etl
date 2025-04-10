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

Inicia el dashboard con:

```bash
streamlit run dashboard.py
```

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

```
news_scraper/
├── news_scraper/                      # Módulo principal del proyecto Scrapy
│   ├── spiders/                       # Spiders para cada fuente de noticias
│   │   ├── quotes_spider.py           # Spider de QuotesToScrape (referencia o demo)
│   │   ├── npr_spider.py              # Spider para NPR
│   │   ├── aljazeera_spider.py        # Spider para Al Jazeera
│   │   └── nyt_spider.py              # Spider para The New York Times (RSS)
│   ├── pipelines.py                   # Limpieza, validación y almacenamiento en JSONL/PostgreSQL
│   ├── items.py                       # Definición de los campos (Scrapy Items)
│   ├── settings.py                    # Configuración de Scrapy (USER_AGENT, DELAY, FEEDS, etc.)
│   ├── middlewares.py                 # (Opcional) Middleware de Scrapy si se usara
│   └── __init__.py                    # Inicializador del módulo Python
│
├── output/                            # Directorio de salida de datos procesados
│   ├── articles_final.jsonl           # Artículos limpios en formato JSONL
│   ├── articles_postgres.csv          # Exportación desde PostgreSQL
│   ├── contar_articulos.py            # Script para contar artículos únicos por fuente
│   ├── exportar_postgres_csv.py       # Script para exportar artículos desde PostgreSQL a CSV
│   ├── exportar_resumen.py            # Script para generar resumen por fuente
│   ├── limpiar_json.py                # Script para limpiar el JSONL de duplicados
│   └── limpiar_postgres.py            # Script para borrar artículos en la tabla PostgreSQL
│
├── datalake/                          # Arquitectura del lago de datos
│   ├── LANDING_ZONE/                  # Datos crudos exportados directamente desde Scrapy
│   │   └── articles_raw.jsonl
│   ├── REFINED_ZONE/                  # Datos limpios exportados de PostgreSQL
│   │   └── articles_postgres.csv
│   └── CONSUMPTION_ZONE/             # Datos agregados resumidos para visualización
│       └── articles_summary.csv
│
├── dashboard.py                       # Dashboard interactivo desarrollado con Streamlit
├── ejecutar_scrapers.bat              # Script por lotes para ejecutar los spiders automáticamente
├── scrapy.cfg                         # Configuración general de Scrapy
├── README.md                          # Documentación técnica del proyecto
└── informe_final.pdf                  # Informe detallado del proyecto (versión académica)

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



