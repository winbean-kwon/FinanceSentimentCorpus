
import scrapy
import pandas as pd
import time
import csv
from datetime import datetime

class NaverFinanceSpider(scrapy.Spider):
    name = 'naver_finance'
    allowed_domains = ['naver.com']
    df = pd.read_csv('test_code.csv')
    codes = df['종목코드'].tolist()

    def start_requests(self):
        self.log('start_requests')
        for code in self.codes:
            for page in range(1, 2):
                url = f'https://finance.naver.com/item/news_news.nhn?code={code}&page={page}&sm=title_entity_id.basic&clusterId='
                time.sleep(0.5)
                yield scrapy.Request(url, callback=self.parse, meta={'code': code})

    def parse(self, response):
        with open('contents.csv', 'a', newline='', encoding='utf-8') as f:
            code = response.meta['code']
            for row in response.css('table.type5 tr'):
                title = row.css('td.title a::text').get()
                source = row.css('td.info::text').get()
                date = row.css('td.date::text').get()
                time.sleep(0.5)
                self.log(title)
                if title and source and date:
                    item = {
                        'code': code,
                        'title': title.strip(),
                        'source': source.strip(),
                        'date': date.strip()
                    }
                    writer = csv.DictWriter(f, fieldnames=item.keys())
                    writer.writerow(item)
                    yield item