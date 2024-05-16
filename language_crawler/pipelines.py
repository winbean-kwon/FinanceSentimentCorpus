# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from sqlalchemy import inspect
from language_crawler.database.models import ArticleOrm
from language_crawler.database.session import SessionLocal
from language_crawler.database.session import engine


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
    def open_spider(self, spider): 
        self.sess = SessionLocal()   
        
        # if not inspect(engine).has_table(engine, 'articles'):
        #     raise Exception("The 'articles' table does not exist. Please run Alembic migrations. \n \
        #                     Please run `alembic upgrade head`. \n \
        #                     For more information, please refer to the README.md file.")
        
    def close_spider(self, spider): 
        self.sess.close()

    def process_item(self, item, spider):
        if item.get('article_id') is None:
            return item
        
        article = ArticleOrm(
            article_id=item['article_id'],
            media_id=item['media_id'],
            media_name=item['media_name'],
            title=item['title'],
            link=item['link'],
            date=item['date'],
            is_origin=item['is_origin'],
            original_id=item.get('origin_id'),
        )
        self.sess.add(article)
        self.sess.commit()
        return item
    