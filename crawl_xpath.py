import scrapy
from scrapy import Spider
import pandas as pd
from datetime import datetime

# class CrawlingItem(scrapy.Item):
#     title = scrapy.Field()
    
#     contents = scrapy.Field()
#     date = scrapy.Field()
#     reporter = scrapy.Field()
#     company = scrapy.Field()

class NaverSpider(scrapy.Spider):
    name = "naver"
    allowed_domains = ['naver.com']
    df = pd.read_csv('stock_code.csv')
    codes = df['종목코드'].tolist()

    # start_urls = [f'https://finance.naver.com/item/news_news.nhn?code={code}&page=&sm=title_entity_id.basic&clusterId=' for code in codes]
    start_urls = ['https://finance.naver.com/item/news_news.nhn?code=005930&page=&sm=title_entity_id.basic&clusterId=']
    
    def parse(self, response):
        news_dates = response.xpath('/html/body/div/table[1]/tbody/tr/td[3]/text()').getall()
        if news_dates:
            base_date = datetime.strptime(news_dates[0].strip(), '%Y.%m.%d.')
        for date in news_dates:
            current_date = datetime.strptime(date.strip(), '%Y.%m.%d.')
            delta = base_date - current_date  # 날짜 차이 계산
            if delta.days >= 3:
                return  # 3일 이상 차이나는 경우 함수 종료
        
        news_title = response.xpath('/html/body/div/table[1]/tbody/tr/td/a/text()').getall()
        for title in news_title:
            print(title)

        news_contents = response.xpath('/html/body/div/table[1]/tbody/tr/td/a/@href').getall()
        for content in news_contents:
            if content:
                content = content.replace("amp;", "")
                print(content)

        news_companies = response.xpath('/html/body/div/table[1]/tbody/tr/td[2]/text()').getall()
        for company in news_companies:
            print(company)

        # for news in news_container:
        #     news_title = news.xpath('./tr/td/a/text()').getall()
            # news_contents = news.xpath('./tr/td/a/@href').getall()
        # title = response.xpath('/html/body/div/table[1]/tbody/tr[11]/td[1]/a/text()').get()
        
        # contents = response.xpath('/html/body/div/table[1]/tbody/tr[1]/td[1]/a/@href').get()
        # if contents:
        #     contents = contents.replace("amp;", "") # 크롤링 안되던 원인이었음
        # date = response.xpath('/html/body/div/table[1]/tbody/tr[1]/td[3]/text()').get()
        # # reporter = response.xpath('XPath_for_reporter').extract() # 뉴스 내용 들어가야 뽑을 수 있을 듯? 근데 가능함
        # company = response.xpath('/html/body/div/table[1]/tbody/tr[1]/td[2]/text()').get()

        # item = CrawlingItem(
        #     'title'=news_title,
        #     # title2=title2,
        #     # contents=contents,
        #     # date=date,
        #     # # reporter=reporter,
        #     # company=company
        # )

        yield {
            'title': news_title,
            'contents': news_contents,
            'dates': news_dates,
            'companies': news_companies,
            
        }
        

# 전체적으로 끌어오자 
# 기간은 3일, 드라이브 실시간 연동 방법 체크
# 