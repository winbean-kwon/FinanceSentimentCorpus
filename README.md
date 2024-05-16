# FinanceSentimentCorpus

## Usage
```bash
export PYTHONPATH=$(pwd):$(pwd)/language_crawler
scrapy runspider spider2.py
```

```bash
scrapy shell https://finance.naver.com/item/news_news.nhn\?code\=265520\&page\=1\&sm\=title_entity_id.basic\&clusterId\=
scrapy shell https://n.news.naver.com/mnews/article/016/0002306239
# 2024-05-10 01:04:27 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://n.news.naver.com/mnews/article/016/0002306239> (referer: None)

scrapy shell "https://n.news.naver.com/mnews/article/016/0002306239" --set=USER_AGENT="Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"

scrapy genspider crawl news_naver
```

### playwright with scrapy

reference : https://oxylabs.io/blog/scrapy-playwright
```bash
poetry add scrapy-playwright
# or pip install scrapy-playwright

playwright install

scrapy startproject language_crawler
```

### Alembic initialization
```bash
cd language_crawler

# edit alembic.ini at Line 63
# sqlalchemy.url = sqlite://-

# edit language_crawler/database/session.py
# DATABASE_URL = f'sqlite://{os.path.join(project_path, "..", "..", "datasets")}/naver_news.db'

# Create a Migration Script:
alembic revision --autogenerate -m "Initial migration"

# Apply Migrations
alembic upgrade head

alembic revision --autogenerate -m "Change column name of article table"
alembic upgrade head
```