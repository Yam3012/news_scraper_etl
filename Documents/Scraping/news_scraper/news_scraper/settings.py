BOT_NAME = "news_scraper"

SPIDER_MODULES = ["news_scraper.spiders"]
NEWSPIDER_MODULE = "news_scraper.spiders"

USER_AGENT = "news_scraper_etl (+https://github.com/Yam3012/news_scraper_etl)"
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

FEEDS = {

}

ITEM_PIPELINES = {
    "news_scraper.pipelines.NewsScraperPipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

