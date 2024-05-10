import scrapy
import re

class ArticlesSpider(scrapy.Spider):
    name = "articlesspider"
    allowed_domains = ["tasty.co"]
    start_urls = ["https://tasty.co"]

    def parse(self, response):
        article_links = response.css('a.nav__submenu-item::attr(href)').getall()
        for link in article_links:
            article_url = response.urljoin(link)
            yield scrapy.Request(article_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css('h1.article__title::text').get()
        author = response.css('div.article__byline__name::text').get()
        date = response.css('time.article__byline__date::attr(datetime)').get()

        if title and author and date:
            yield {
                'title': title.strip(),
                'author': author.strip(),
                'date': date.strip(),
            }