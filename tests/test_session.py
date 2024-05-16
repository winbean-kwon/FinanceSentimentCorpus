import unittest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from language_crawler.database.models import ArticleOrm

class TestSession(unittest.TestCase):
    def setUp(self):
        DATABASE_URL = 'sqlite:///datasets/test.db'
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        self.session = SessionLocal()

    def tearDown(self):
        self.session.close()

    def test_query_all_articles(self):
        articles = self.session.query(ArticleOrm).all()
        self.assertEqual(len(articles), 0)  # Assuming there are no articles in the test database

    def test_insert_article(self):
        article = ArticleOrm(title='Test Article', content='This is a test article')
        self.session.add(article)
        self.session.commit()

        articles = self.session.query(ArticleOrm).all()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Test Article')
        self.assertEqual(articles[0].content, 'This is a test article')

if __name__ == '__main__':
    unittest.main()