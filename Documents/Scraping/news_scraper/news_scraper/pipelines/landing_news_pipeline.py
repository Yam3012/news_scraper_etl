import os
import json
from itemadapter import ItemAdapter

class LandingPipeline:
    def open_spider(self, spider):
        os.makedirs('datalake/LANDING_ZONE', exist_ok=True)
        self.file = open('datalake/LANDING_ZONE/articles_raw.json', 'a', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if not adapter.get('title') or not adapter.get('url') or not adapter.get('source'):
            spider.logger.warning(f"Artículo incompleto descartado en Landing: {item}")
            return item

        json.dump(dict(item), self.file, ensure_ascii=False)
        self.file.write('\n')

        print(f"✅ [Landing] Guardado en JSON: {item['title']}")
        return item