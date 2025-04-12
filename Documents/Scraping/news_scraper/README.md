# NewsScraper ETL System

Este proyecto implementa un sistema completo de Extracción, Transformación y Carga (ETL) para noticias, utilizando **Scrapy**, **PostgreSQL**, una **arquitectura de lago de datos** y visualización con **Streamlit**.

---

## Objetivos del Proyecto

- Extraer automáticamente artículos desde varias fuentes web.
- Validar y transformar datos con Scrapy Items y Pipelines.
- Almacenar datos en formatos estructurados: JSONL y PostgreSQL.
- Organizar los datos bajo una arquitectura de Data Lake.
- Visualizar estadísticas clave en un panel interactivo con filtros dinámicos.
- Enriquecer los datos con una API externa (clima actual de una ciudad).

---

## Tecnologías y Librerías Usadas

- **Python 3.10+**
- **Scrapy**
- **PostgreSQL**
- **psycopg2**
- **Streamlit**
- **Requests**
- **dotenv**
- **JSON / JSONL**

---

## Instalación

```bash
pip install -r requirements.txt
```

### Configura PostgreSQL

```sql
CREATE DATABASE scraping_db;
```

No es necesario crear tablas manualmente: los pipelines crean automáticamente:
- `articles_refined`
- `articles_consumption`

---

##  Ejecución del Scraper

```bash
scrapy crawl aljazeera
scrapy crawl npr
scrapy crawl nyt
```

O usa el script:

```bash
ejecutar_scrapers.bat
```

---

##  Limpieza y Validación

```bash
cd output
python contar_articulos.py
python limpiar_postgres.py
```

---

##  Exportar a CSV desde PostgreSQL

```bash
python exportar_postgres_csv.py
```

---

##  Procesamiento con Pipelines

Los datos pasan secuencialmente por:

1. **LandingPipeline:** Guarda JSONL crudo en `datalake/LANDING_ZONE/`
2. **RefinedPipeline:** Limpia campos, guarda en `articles_refined` y `REFINED_ZONE/`
3. **ConsumptionPipeline:** Inserta en `articles_consumption` y `CONSUMPTION_ZONE/`

Configurados en `settings.py`:

```python
ITEM_PIPELINES = {
    "news_scraper.pipelines.landing_news_pipeline.LandingPipeline": 100,
    "news_scraper.pipelines.refined_news_pipeline.RefinedPipeline": 200,
    "news_scraper.pipelines.consumption_news_pipeline.ConsumptionPipeline": 300,
}
```

---

##  Arquitectura del Lago de Datos

```
datalake/
├── LANDING_ZONE/         # Datos crudos (.jsonl)
├── REFINED_ZONE/         # Datos limpios (.jsonl)
└── CONSUMPTION_ZONE/     # Datos listos para análisis (.jsonl)
```

---

##  Visualización con Streamlit

```bash
cd dashboard
streamlit run dashboard.py
```

Variables en `.env`:

```env
DB_HOST=localhost
DB_USER=postgres
DB_PASSWORD=Root123$$
DB_DATABASE=scraping_db
```

---

##  Funcionalidades del Dashboard

- Filtro por fecha (`st.date_input`)
- Total de artículos (`st.metric`)
- Tabla por fuente (`st.dataframe`)
- Gráfico (`st.bar_chart`)
- Clima actual por ciudad (API OpenWeatherMap)

---

##  Estructura del Proyecto

```
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
├── output/
├── ejecutar_scrapers.bat
├── requirements.txt
├── README.md
└── informe_final.pdf
```

---

##  Scripts Auxiliares

- `exportar_postgres_csv.py`
- `exportar_resumen.py`
- `contar_articulos.py`
- `limpiar_postgres.py`

---

##  Buenas Prácticas Aplicadas

- `USER_AGENT` personalizado
- Respeto a `robots.txt`
- `DOWNLOAD_DELAY = 2`
- `AUTOTHROTTLE` habilitado
- Codificación UTF-8
- Validación mínima en todos los pipelines

---

##  Licencia

Desarrollado por **Yamil Gamarra López**  
Maestría en Ciencia de Datos e Inteligencia Artificial – Abril 2025


