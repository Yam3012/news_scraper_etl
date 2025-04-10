import scrapy
from news_scraper.items import NewsScraperItem
from datetime import datetime
import os
import json

class AlJazeeraSpider(scrapy.Spider):
    name = 'aljazeera'
    allowed_domains = ['aljazeera.com']
    start_urls = ['https://www.aljazeera.com/news/']

    def parse(self, response):
        articles = response.css('div.gc__content')
        existing_urls = self.get_existing_urls()

        for article in articles:
            title = article.css('h3.gc__title span::text').get()
            url = article.css('a::attr(href)').get()
            if url and not url.startswith('http'):
                url = response.urljoin(url)

            summary = article.css('p::text').get()
            date = datetime.today().strftime('%Y-%m-%d')

            if not url or url in existing_urls:
                continue

            print(f"🗞️ {title} | {url}")

            item = NewsScraperItem(
                title=title.strip() if title else '',
                url=url,
                date=date,
                source='AlJazeera',
                summary=summary.strip() if summary else ''
            )
            yield item




    def get_existing_urls(self):
        path = 'output/articles.json'
        if not os.path.exists(path):
            return set()
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return {article['url'] for article in data}
        except:
            return set()



 
