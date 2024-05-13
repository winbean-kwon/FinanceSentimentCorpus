import scrapy
import pandas as pd
import time
import csv
from datetime import datetime

class NaverFinanceSpider(scrapy.Spider):
    name = 'naver_finance'
    allowed_domains = ['naver.com']
    df = pd.read_csv('stock_code.csv')
    codes = df['종목코드'].tolist()
    # start_urls = [f'https://finance.naver.com/item/news_news.nhn?code={code}&page=&sm=title_entity_id.basic&clusterId=' for code in codes]
    start_urls = [f'https://finance.naver.com/item/news_news.naver?code=126600&page={index}&sm=title_entity_id.basic&clusterId=' for index in range(1,3)] # 테스트용

    def parse(self, response):
        with open('contents.csv', 'a', newline='', encoding='utf-8') as f:
            for row in response.css('table.type5 tr'):
                title = row.css('td.title a::text').get()
                source = row.css('td.info::text').get()
                date = row.css('td.date::text').get()
                time.sleep(1)
                if title and source and date:
                    item =  {
                        'title': title.strip(),
                        'source': source.strip(),
                        'date': date.strip()
                    }
                    with open('contents.csv', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=item.keys())
                        writer.writerow(item)
                        yield item

            # 다음 페이지로 이동
            # for index in range(1, 10):
            #     next_page = f'https://finance.naver.com/item/news_news.naver?code=126600&page={index}&clusterId='
            #     yield scrapy.Request(next_page, self.parse)
            

# 뉴스 적은애: 001045
# 테스트용 : 126600