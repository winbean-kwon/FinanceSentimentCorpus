from time import sleep
from typing import Iterable, Union

import scrapy
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
from twisted.python.failure import Failure

from language_crawler.database.models import ArticleOrm
from language_crawler.database.session import SessionLocal 

from newspaper import Article


ArticleId = Union[str, int]
OfficeId = Union[str, int]

def _get_target_url(article_id: ArticleId, office_id: OfficeId):
    article_id = int(article_id) if isinstance(article_id, str) else article_id
    office_id = int(office_id) if isinstance(office_id, str) else office_id
    return f"https://n.news.naver.com/mnews/article/{office_id:03d}/{article_id:010d}"

class NewsContents(scrapy.Spider):
    name = "news_contents"
    allowed_domains = ["naver.com"]
    custom_settings = dict(
        DOWNLOADER_MIDDLEWARES={
            "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
            "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
            "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
        },
        FAKEUSERAGENT_PROVIDERS=[
            "scrapy_fake_useragent.providers.FakerProvider",
            "scrapy_fake_useragent.providers.FakeUserAgentProvider",
            "scrapy_fake_useragent.providers.FixedUserAgentProvider",
        ],
    )

    def start_requests(self) -> Iterable[Request]:
        session = SessionLocal()
        articles = session.query(ArticleOrm).all()
        for article in articles:
            self.log(article)
            yield Request(
                _get_target_url(article.article_id, article.media_id),
                meta=dict(article_id=article.article_id),
                callback=self.parse,
                errback=self.errback,
            )
            sleep(1)
    
    async def parse(self, response: HtmlResponse):
        # Print out the user-agent of the request to check they are random
        self.log(response.request.headers.get("User-Agent"))
        self.log(response.url)

        article = Article(response.url)
        article.set_html(response.text)
        article.parse()

        # Extracted data
        title = article.title
        text = article.text
        authors = article.authors
        publish_date = article.publish_date

        # Log or save the extracted data
        self.log(f"Title: {title}")
        self.log(f"Text: {text[:200]}...")  # Log first 200 characters of the text
        self.log(f"Authors: {authors}")
        self.log(f"Publish Date: {publish_date}")


    async def errback(self, failure: Failure):
        self.log(type(failure))
        self.log(failure)
