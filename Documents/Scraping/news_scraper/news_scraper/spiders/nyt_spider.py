import scrapy
from scrapy.spiders import XMLFeedSpider
from news_scraper.items import NewsScraperItem
from datetime import datetime
import email.utils

class NYTSpider(XMLFeedSpider):
    name = 'nyt'
    allowed_domains = ['rss.nytimes.com']
    start_urls = ['https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml']
    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, node):
        item = NewsScraperItem()
        item['title'] = node.xpath('title/text()').get()
        item['url'] = node.xpath('link/text()').get()

        pub_date = node.xpath('pubDate/text()').get()
        if pub_date:
            parsed_date = datetime(*email.utils.parsedate(pub_date)[:6])
            item['date'] = parsed_date.date().isoformat()
        else:
            item['date'] = None

        item['source'] = 'The New York Times'
        item['summary'] = node.xpath('description/text()').get()
        return item





 
