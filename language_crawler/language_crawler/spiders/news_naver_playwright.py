import scrapy
import pandas as pd
from datetime import datetime

from scrapy_playwright.page import PageMethod

class NewsNaverPlaywright(scrapy.Spider):

    name = "news_naver_playwright"
    allowed_domains = ['naver.com']
    df = pd.read_csv('../datasets/test_code.csv')
    codes = df['종목코드'].tolist()

    def start_requests(self):
        for code in self.codes[:2]:
            target_url = self._get_news_url(code)

            screentshot_path = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{code:06d}.png'
            yield scrapy.Request(
                target_url,
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod("screenshot", path=screentshot_path, full_page=True),
                    ],
                    errback=self.errback,
                    code=code,
                ),
            )

            # for page in range(1, 10):
            #     yield scrapy.Request(url, callback=self.parse, meta={'code': code})
        
    def _get_news_url(self, code: str):
        return f"https://finance.naver.com/item/news.naver?code={code:06d}"

    async def parse(self, response):
        page = response.meta["playwright_page"]
        print(page)
        # await page.close()
        
    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()