import psycopg2
import csv

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname="scraping_db",
    user="postgres",
    password="Root123$$",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Ejecutar consulta
cur.execute("SELECT id, title, url, date, source, summary FROM articles ORDER BY id ASC")
rows = cur.fetchall()

# Exportar a CSV (respetando columnas)
with open("articles_postgres.csv", mode="w", newline='', encoding="utf-8") as file:
    writer = csv.writer(file, quoting=csv.QUOTE_ALL)
    writer.writerow(['id', 'title', 'url', 'date', 'source', 'summary'])  # encabezados
    for row in rows:
        writer.writerow(row)

print("✅ Datos exportados correctamente a output/articles_postgres.csv")

# Cerrar conexión
cur.close()
conn.close()
