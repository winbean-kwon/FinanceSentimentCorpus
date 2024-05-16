import time
import scrapy
import pandas as pd
import os
import re

from scrapy.http.response.html import HtmlResponse

from language_crawler.items import ArticleItem

class FinanceNewsList(scrapy.Spider):
    name = os.path.basename(__file__).replace('.py', '')
    allowed_domains = ['naver.com']

    df = pd.read_csv('../datasets/test_code.csv')
    codes = df['종목코드'].tolist()

    def start_requests(self):
        for code in self.codes[:2]:
            target_url = self._get_news_url(126600)

            yield scrapy.Request(
                target_url,
                meta=dict(code=code, page=1),
                callback=self.parse, 
                errback=self.errback,
            )
        
    def _get_news_url(self, code: str, page: str=1):
        return f"https://finance.naver.com/item/news_news.naver?code={code:06d}&page={page}"


    async def parse(self, response: HtmlResponse):
        meta = response.meta
        current_page = meta['page']

        # Check end of page
        info_text_area = response.css('div > table > tbody > tr > td > div').get()
        if info_text_area and '뉴스가 없습니다.' in info_text_area:
            self.log(f"End of page reached for {meta['code']}")
            return

        if not info_text_area:
            self.log(f"Failed to find info_text_area for {meta['code']}. Performing full search.")
            if '뉴스가 없습니다.' in response.text:
                self.log(f"End of page reached for {meta['code']}")
                return
        
        processed_ids = set()
        
        for row in response.css('table.type5 tr'):
            content_url = row.css('td.title a::attr(href)').extract_first()
            title = row.css('td.title a::text').get()
            source = row.css('td.info::text').get()
            date = row.css('td.date::text').get()

            article_id = None
            office_id = None
            if content_url:
                article_id, office_id = self._extract_article_and_office_ids(content_url)
                if article_id and office_id:
                    if f"{office_id}{article_id}" in processed_ids:
                        self.log(f"Skipping duplicate article: {title}")
                        self.log(f'------' * 5)
                        continue
                    else:
                        processed_ids.add(f"{office_id}{article_id}")
                    self.log(f"Article ID: {article_id}, Office ID: {office_id}")
            else:
                self.log(f"Failed to extract article_id and office_id from content_url: {content_url}")
            
            row_class = row.attrib.get('class', '')
            is_relation_origin = False
            is_related = False
            if 'relation_tit' in row_class:
                is_relation_origin = True
            elif 'relation_lst' in row_class:
                is_related = True

            relation_origin_id = ''
            self.log(f"Content URL: {content_url}")
            if is_related:
                self.log(f"Related article found: {title}")
                office_id, article_id = self._extract_cluster_ids(row_class)
                if office_id and article_id:
                    self.log(f"Office ID: {office_id}, News ID: {article_id}")
                relation_origin_id = f"{office_id}{article_id}"
            else:
                self.log(f"Main article found: {title}")
            
            yield ArticleItem(
                article_id=article_id,
                media_id=office_id,
                media_name=source,
                title=title,
                link=content_url,
                date=date,
                is_origin=is_relation_origin,
                origin_id=relation_origin_id if is_related else None,
            )
            self.log(f'------' * 5)

        time.sleep(0.5)

        yield scrapy.Request(
            self._get_news_url(meta['code'], current_page + 1),
            meta=dict(code=meta['code'], page=current_page + 1),
            callback=self.parse, 
            errback=self.errback,
        )

    def _is_related_article(self, row_class: str) -> bool:
        return 'relation_tit' in row_class or 'relation_lst' in row_class

    def _extract_cluster_ids(self, row_class: str):
        # Extract clusterId
        # "<tr class="relation_lst _clusterId0310000829596">" 이런 형식인데 _clusterId0310000829596 에서 
        # 0310000829596 이부분을 추출하고 싶어, 이 부분의 앞의 3자리는 언론사 고유 id 이고 뒷자리는 모두 뉴스 기사 고유 ID야.
        match = re.search(r'_clusterId(\d{3})(\d+)', row_class)
        if match:
            return match.group(1), match.group(2)
        return None, None

    def _extract_article_and_office_ids(self, content_url: str):
        # "/item/news_read.naver?article_id=0000365184&office_id=374&code=060310&page=1&sm=" 
        # 에서 office_id와 article_id를 추출하고 싶어.
        match = re.search(r'article_id=(\d+)&office_id=(\d+)', content_url)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    async def errback(self, failure):
        self.log(type(failure))
        meta = failure.request.meta