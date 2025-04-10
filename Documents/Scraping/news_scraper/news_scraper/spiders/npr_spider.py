import scrapy
from news_scraper.items import NewsScraperItem
from datetime import datetime
import os
import json

class NPRSpider(scrapy.Spider):
    name = 'npr'
    allowed_domains = ['npr.org']
    start_urls = ['https://www.npr.org/sections/news/']

    def parse(self, response):
        articles = response.css('article.item')
        existing_urls = self.get_existing_urls()

        for article in articles:
            url = article.css('h2.title a::attr(href)').get()
            title = article.css('h2.title a::text').get()
            summary = article.css('p.teaser a::text').get()
            date = datetime.today().strftime('%Y-%m-%d')

            if not url or url in existing_urls:
                continue

            print(f"📰 {title} | {url}")

            item = NewsScraperItem(
                title=title.strip() if title else '',
                url=url,
                date=date,
                source='NPR',
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



 
