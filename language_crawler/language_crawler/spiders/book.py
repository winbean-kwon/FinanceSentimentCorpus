import scrapy

from language_crawler.items import Book


class BooksSpider(scrapy.Spider):
   """Class for scraping books from https://books.toscrape.com/"""

   name = "books"

   def start_requests(self):
       url = "https://books.toscrape.com/"
       yield scrapy.Request(
           url,
           meta=dict(
               playwright=True,
               playwright_include_page=True,
               errback=self.errback,
           ),
       )

   async def parse(self, response):
       page = response.meta["playwright_page"]
       await page.close()

       for book in response.css("article.product_pod"):
           book = Book(
               title=book.css("h3 a::attr(title)").get(),
               price=book.css("p.price_color::text").get(),
           )
           yield book

   async def errback(self, failure):
       page = failure.request.meta["playwright_page"]
       await page.close()