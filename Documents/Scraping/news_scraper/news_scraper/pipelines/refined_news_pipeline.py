import os
import json
import psycopg2
from itemadapter import ItemAdapter

class RefinedPipeline:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname='scraping_db',
            user='postgres',
            password='Root123$$',
            host='localhost',
            port='5432'
        )
        self.cursor = self.conn.cursor()
        os.makedirs('datalake/REFINED_ZONE', exist_ok=True)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles_refined (
                id SERIAL PRIMARY KEY,
                title TEXT,
                url TEXT UNIQUE,
                date TEXT,
                source TEXT,
                summary TEXT
            );
        """)
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        item = self.transform_item(adapter)

        if not item.get('title') or not item.get('url') or not item.get('source'):
            spider.logger.warning(f"Artículo inválido descartado en Refined: {item}")
            return item

        try:
            self.cursor.execute("""
                INSERT INTO articles_refined (title, url, date, source, summary)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """, (
                item['title'],
                item['url'],
                item['date'],
                item['source'],
                item['summary']
            ))
            print(f"✅ [Refined] Insertado en PostgreSQL: {item['title']}")
        except Exception as e:
            spider.logger.error(f"❌ Error al insertar en PostgreSQL Refined: {e}")

        with open('datalake/REFINED_ZONE/articles_refined.json', 'a', encoding='utf-8') as f:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

        return item

    def transform_item(self, adapter):
        return {
            'title': adapter.get('title', '').strip(),
            'url': adapter.get('url', '').strip(),
            'date': adapter.get('date', '').strip(),
            'source': adapter.get('source', '').strip(),
            'summary': adapter.get('summary', '').strip()
        }