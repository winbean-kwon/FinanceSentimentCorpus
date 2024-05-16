# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    article_id = scrapy.Field()
    media_id = scrapy.Field()
    media_name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    date = scrapy.Field()
    is_origin = scrapy.Field()
    origin_id = scrapy.Field()
