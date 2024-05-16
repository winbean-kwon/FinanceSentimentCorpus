# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pprint import pprint
from itemadapter import ItemAdapter


class LanguageCrawlerPipeline:
    """
    Typical uses of item pipelines are:
    - cleansing HTML data
    - validating scraped data (checking that the items contain certain fields)
    - checking for duplicates (and dropping them)
    - storing the scraped item in a database
    """
    def open_spider(self, spider): ...
    def close_spider(self, spider): ...
    def process_item(self, item, spider):
        return item

class FinanceNewsListPipeline:
    """
    Typical uses of item pipelines are:
    - cleansing HTML data
    - validating scraped data (checking that the items contain certain fields)
    - checking for duplicates (and dropping them)
    - storing the scraped item in a database
    """
    def open_spider(self, spider): ...
    def close_spider(self, spider): ...
    def process_item(self, item, spider):
        pprint(item)