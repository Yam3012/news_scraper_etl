import scrapy
from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader

class NewsScraperItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())
    source = scrapy.Field(output_processor=TakeFirst())
    summary = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
