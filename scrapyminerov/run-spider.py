from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapyminerov.spiders.flats import FlatSpider


process = CrawlerProcess(get_project_settings())
process.crawl(FlatSpider)
process.start()
