# output/exportar_resumen.py

import psycopg2
import csv

conn = psycopg2.connect(
    dbname="scraping_db",
    user="postgres",
    password="Root123$$",
    host="localhost"
)
cur = conn.cursor()

cur.execute("SELECT source, COUNT(*) FROM articles GROUP BY source")
rows = cur.fetchall()

with open("datalake/CONSUMPTION_ZONE/articles_summary.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["source", "total_articles"])
    writer.writerows(rows)

conn.close()

