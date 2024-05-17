# import scrapy
# import pandas as pd
# from datetime import datetime

# class NaverFinanceSpider(scrapy.Spider):
#     name = 'naver_finance'
#     allowed_domains = ['naver.com']
#     df = pd.read_csv('stock_code.csv')
#     codes = df['종목코드'].tolist()
#     start_urls = [f'https://finance.naver.com/item/news_news.nhn?code={code}&page=&sm=title_entity_id.basic&clusterId=' for code in codes]
#     # start_urls = ['https://finance.naver.com/item/news_news.naver?code=005930&page=1&clusterId=']

#     def parse(self, response):
#         for row in response.css('table.type5 tr'):
#             title = row.css('td.title a::text').get()
#             source = row.css('td.info::text').get()
#             date = row.css('td.date::text').get()
#             if title and source and date:
#                 yield {
#                     'title': title.strip(),
#                     'source': source.strip(),
#                     'date': date.strip()
#                 }

#         # 다음 페이지로 이동
#         for index in range(1, 10):
#             next_page = f'https://finance.naver.com/item/news_news.naver?code={code}&page={index}&clusterId='
#             yield scrapy.Request(next_page, self.parse)
            


# import scrapy
# import pandas as pd
# import time
# import csv
# from datetime import datetime

# class NaverFinanceSpider(scrapy.Spider):
#     name = 'naver_finance'
#     allowed_domains = ['naver.com']
#     df = pd.read_csv('test.csv')
#     codes = df['종목코드'].tolist()

#     def start_requests(self):
#         for code in self.codes:
#             for page in range(1, 10):
#                 url = f'https://finance.naver.com/item/news_news.nhn?code={code}&page={page}&sm=title_entity_id.basic&clusterId='
#                 yield scrapy.Request(url, callback=self.parse, meta={'code': code})

#     def parse(self, response):
#         with open('contents.csv', 'a', newline='', encoding='utf-8') as f:
#             code = response.meta['code']
#             for row in response.css('table.type5 tr'):
#                 title = row.css('td.title a::text').get()
#                 source = row.css('td.info::text').get()
#                 date = row.css('td.date::text').get()
#                 time.sleep(0.5)
#                 if title and source and date:
#                     item = {
#                         'code': code,
#                         'title': title.strip(),
#                         'source': source.strip(),
#                         'date': date.strip()
#                     }
#                     writer = csv.DictWriter(f, fieldnames=item.keys())
#                     writer.writerow(item)
#                     yield item
