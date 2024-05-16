from time import sleep
from typing import Iterable, Union
from datetime import datetime

import scrapy
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
from twisted.python.failure import Failure
from bs4 import BeautifulSoup

from language_crawler.database.models import ArticleContentOrm, ArticleOrm
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
        articles = session\
            .query(ArticleOrm)\
            .filter(ArticleOrm.latest_scraped_at == None)\
            .all()
        for article in articles:
            self.log(article)
            yield Request(
                _get_target_url(article.article_id, article.media_id),
                meta=dict(
                    article_id=article.article_id,
                    media_id=article.media_id,
                ),
                callback=self.parse,
                errback=self.errback,
            )
            sleep(1)
    
    async def parse(self, response: HtmlResponse):
        # Print out the user-agent of the request to check they are random
        self.log(response.request.headers.get("User-Agent"))
        self.log(response.url)

        title = response.xpath("/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[2]/h2/span/text()").get()
        content_html = response.xpath("/html/body/div[1]/div[2]/div/div[1]/div[1]/div[2]/div[1]/article").get()
        soup = BeautifulSoup(content_html, "html.parser")
        for tag in soup(['img', 'span', 'strong', 'em', 'div']):
            tag.decompose()
        contnet_text = soup.get_text()
        
        media_end_head_info_datestamp = response.xpath("/html/body/div[1]/div[2]/div/div[1]/div[1]/div[1]/div[3]/div[1]")
        publish_date_html = media_end_head_info_datestamp.xpath("div[1]/span/@data-date-time").get()
        publish_date = datetime.strptime(publish_date_html, "%Y-%m-%d %H:%M:%S") if publish_date_html else None
        modified_date_html = media_end_head_info_datestamp.xpath("div[2]/span/@data-date-time").get()
        modified_date = datetime.strptime(modified_date_html, "%Y-%m-%d %H:%M:%S") if modified_date_html else None

        self.log(title)
        self.log(contnet_text)
        self.log(publish_date)
        self.log(modified_date)
        
        if not title or not content_html:
            self.log("Failed to extract title or content_html")
            return
        
        session = SessionLocal()
        article = session.query(ArticleOrm).filter_by(
            article_id=response.meta['article_id'],
            media_id=response.meta['media_id']
        ).first()
        article.latest_scraped_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.commit()
        
        article_content = ArticleContentOrm(
            article_id=article.article_id,
            media_id=article.media_id,
            html=response.text,
            content=contnet_text,
            title=title,
            language='ko',
        )
        
        session.close()
                
    async def errback(self, failure: Failure):
        self.log(type(failure))
        self.log(failure)
