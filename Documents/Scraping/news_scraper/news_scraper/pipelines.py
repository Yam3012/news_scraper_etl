import json
import psycopg2
from itemadapter import ItemAdapter

class NewsScraperPipeline:
    def open_spider(self, spider):
        # Conexión a PostgreSQL
        self.conn = psycopg2.connect(
            dbname='scraping_db',
            user='postgres',
            password='Root123$$',
            host='localhost',
            port='5432'
        )
        self.cursor = self.conn.cursor()

        # Archivo JSONL para acumulación
        self.json_file = open('output/articles_final.jsonl', 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.json_file.close()
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        title = adapter.get('title', '').strip()
        url = adapter.get('url', '').strip()
        date = adapter.get('date', '').strip()
        source = adapter.get('source', '').strip()
        summary = adapter.get('summary', '').strip()

        # Validación mínima
        if not title or not url or not source:
            spider.logger.warning(f"Artículo incompleto descartado: {item}")
            return item

        # Guardar en PostgreSQL (evitar duplicados por URL)
        try:
            self.cursor.execute("""
                INSERT INTO articles (title, url, date, source, summary)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """, (title, url, date, source, summary))
        except Exception as e:
            spider.logger.error(f"❌ Error al insertar en PostgreSQL: {e}")

        # Guardar en JSONL (solo si no está duplicado)
        try:
            if not self._url_exists_in_jsonl(url):
                json.dump({
                    'title': title,
                    'url': url,
                    'date': date,
                    'source': source,
                    'summary': summary
                }, self.json_file, ensure_ascii=False)
                self.json_file.write('\n')
        except Exception as e:
            spider.logger.error(f"❌ Error al escribir en JSONL: {e}")

        return item

    def _url_exists_in_jsonl(self, url):
        """Verifica si una URL ya existe en el archivo JSONL."""
        try:
            with open('output/articles_final.jsonl', 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        article = json.loads(line)
                        if article.get('url') == url:
                            return True
                    except json.JSONDecodeError:
                        continue
        except FileNotFoundError:
            return False
        return False







