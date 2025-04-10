import psycopg2

try:
    conn = psycopg2.connect(
        dbname="scraping_db",
        user="postgres",
        password="Root123$$",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles;")
    conn.commit()
    print("✅ Base de datos limpiada correctamente.")
except Exception as e:
    print("❌ Error:", e)
finally:
    cursor.close()
    conn.close()
