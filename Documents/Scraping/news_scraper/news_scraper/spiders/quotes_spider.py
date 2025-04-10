import scrapy
from news_scraper.items import NewsScraperItem
from datetime import datetime
import os
import json

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/page/1/']

    def parse(self, response):
        quotes = response.css('div.quote')
        existing_urls = self.get_existing_urls()

        for quote in quotes:
            text = quote.css('span.text::text').get()
            author = quote.css('small.author::text').get()
            url = response.url
            summary = f'Quote by {author}'
            date = datetime.today().strftime('%Y-%m-%d')

            if url in existing_urls:
                continue

            print(f"💬 {text} | {url}")

            item = NewsScraperItem(
                title=text.strip() if text else '',
                url=url,
                date=date,
                source='QuotesToScrape',
                summary=summary
            )
            yield item

        # Paginación
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

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


