# FinanceSentimentCorpus

## Usage
```bash
poetry install
poetry shell
alembic upgrade head
scrapy crawl finance_news_list 
scrapy crawl news_contents
```