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
    is_related = Column(Boolean, nullable=False)
    original_id = Column(String, nullable=True)