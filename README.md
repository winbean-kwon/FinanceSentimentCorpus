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

## Scrapy-extension
- [scrapy-fake-agent](https://github.com/alecxe/scrapy-fake-useragent)
- [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright)

## html compression algorithm

The crawled HTML code is stored as binary, compressed using the `lzma` algorithm. [Simple tests](https://chat.openai.com/share/a0a256b4-6e04-4920-8f4e-7b7285977476) showed that among `lz4`, `gzip`, `bz2`, and `lzma`, `lzma` had the best compression ratio. Compression time was not considered.