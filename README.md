# FinanceSentimentCorpus

## Usage
```bash
poetry install
poetry shell
# 반드시 datasets/articles.db 를 먼저 생성해야함
alembic upgrade head

# TASK1: 네이버 뉴스 링크 리스트를 datasets/articles.db 에 저장
scrapy crawl finance_news_list 

# TASK2: 저장된 네이버 뉴스 링크 리스트에서 하나씩 뉴스 본문 파싱
scrapy crawl news_contents
```