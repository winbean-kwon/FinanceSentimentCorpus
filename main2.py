
import scrapy
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv
from datetime import datetime

class NaverFinanceSpider(scrapy.Spider):
    name = 'naver_finance'
    allowed_domains = ['naver.com']
    df = pd.read_csv('datasets/test_code.csv')
    codes = df['종목코드'].tolist()

    def _news_list_url(self, code: str):
        return f"https://finance.naver.com/item/news.naver?code={code:06d}"

    def start_requests(self):
        for code in self.codes:
            self.log(f'start_requests...for {code:06d}')
            
            # for page in range(1, 2):
            #     url = f'https://finance.naver.com/item/news_news.nhn?code={code}&page={page}&sm=title_entity_id.basic&clusterId='
            #     time.sleep(0.5)
            #     yield scrapy.Request(url, callback=self.parse, meta={'code': code})

    def parse(self, response):
        with open('datasets/contents.csv', 'a', newline='', encoding='utf-8') as f:
            code = response.meta['code']
            for row in response.css('table.type5 tr'):
                content_url = row.css('td.title a::attr(href)').extract_first()
                title = row.css('td.title a::text').get()
                source = row.css('td.info::text').get()
                date = row.css('td.date::text').get()

                self.log(title)
                if title and source and date:
                    item = {
                        'code': code,
                        'title': title.strip(),
                        'source': source.strip(),
                        'date': date.strip(),
                        'content_url': content_url.strip()
                    }
                    writer = csv.DictWriter(f, fieldnames=item.keys())
                    writer.writerow(item)
                    yield item

                time.sleep(0.5)

def parse_content_url(self, response):
    """
    >>> html_content = response.xpath('/html').extract_first()
    "<html><head><script>top.location.href='https://n.news.naver.com/mnews/article/016/0002306239';</script></head></html>"
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> script_tag = soup.find('script')
    >>> url = script_tag.text.split("'")[1]  
    """
    pass