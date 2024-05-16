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

#### Scrapy-extension
1. [scrapy-fake-agent](https://github.com/alecxe/scrapy-fake-useragent)
2. [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright)

#### html compression algorithm
크롤링한 html 코드를 바이너리 그대로 저장하는데, 이때 `lzma` 알고리즘을 통해 압축해서 저장한다. 
간단한 테스트에서 `lz4, gzip, bz2, lzma` 중 `lzma` 가 가장 압축률이 좋았다. 압축 시간은 상관하지 않았다.
> [results](https://chat.openai.com/share/a0a256b4-6e04-4920-8f4e-7b7285977476)
