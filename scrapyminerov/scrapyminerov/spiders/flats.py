import scrapy
import psycopg2
from scrapy import signals
from time import sleep

rootUrl = 'https://books.toscrape.com'


class FlatSpider(scrapy.Spider):
    name = 'flats'

    def __init__(self):
        self.data = []

        while True:
            try:
                self.connection = psycopg2.connect(
                    host="db",
                    port="5432",
                    user="root",
                    password="123",
                    database="scrapy"
                )

                sleep(5)
                break
            except:
                pass

        self.cursor = self.connection.cursor()

        self.cursor.execute("SELECT version();")
        version = self.cursor.fetchone()[0]
        print("PostgreSQL version:", version)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                image TEXT,
                title TEXT
            )
        """)

        self.connection.commit()

    def start_requests(self):
        for i in range(1, 20):
            yield scrapy.Request(url=f'{rootUrl}/catalogue/page-{i}.html', callback=self.parse)

    def parse(self, response):
        for article in response.css('article.product_pod'):
            self.data.append({
                "image": article.css('.thumbnail::attr(src)').get(),
                "title": article.css('a::text').get()
            })

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed,
                                signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        for item in self.data:
            image = item["image"]
            title = item["title"]

            self.cursor.execute(
                "INSERT INTO books (image, title) VALUES (%s, %s)", (rootUrl + image[2:], title))

        # Commit the changes to the database
        self.connection.commit()

        # Close the cursor and the connection
        self.cursor.close()
        self.connection.close()
