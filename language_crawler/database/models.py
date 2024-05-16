from sqlalchemy import Column, Integer, String, Boolean
from language_crawler.database.base import Base

class ArticleOrm(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, nullable=False)
    media_id = Column(String, nullable=False)
    media_name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    date = Column(String, nullable=False)
    is_origin = Column(Boolean, nullable=False)
    original_id = Column(String, nullable=True)
    latest_scraped_at = Column(String, nullable=True)

class ArticleContentOrm(Base):
    __tablename__ = 'article_contents'
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(String, nullable=False)
    media_id = Column(String, nullable=False)
    html = Column(String, nullable=True)
    content = Column(String, nullable=True)
    title = Column(String, nullable=True)
    language = Column(String, nullable=False)