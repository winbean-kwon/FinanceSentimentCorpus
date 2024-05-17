# 시장의나침판

<p align="center">
  <img src="assets/main.png" alt="Logo">
</p>

이 프로젝트는 뉴스 기사를 크롤링하여 주식 및 금융 상품의 방향성을 예측하고 거래하는 알고리즘 트레이딩 모델을 개발하는 것을 목적으로 합니다.
또한, `LangChain`과 `Transformer(HuggingFace)` 모델을 활용하여 금융 도메인에서 발생하는 언어 데이터를 심층 분석하고, 시장의 비효율성을 탐지하는 것을 목표로 합니다.

## 주요 기능
- **가격 변동 원인 분석**: 보유 자산의 가격 변동 원인을 애널리스트 보고서, 전자 공시, 뉴스 데이터를 통해 추론하고, 이를 자동으로 보고서로 작성합니다.
- **실시간 데이터 수집 및 초단기 매매**: 실시간으로 애널리스트 보고서, 전자 공시, 뉴스 데이터를 수집하여 초단기 방향성 매매 전략을 실행합니다.

이 프로젝트는 고급 자연어 처리(NLP) 기술을 사용하여 금융 시장에서 발생하는 정보 비대칭성을 줄이고, 정량적 거래 전략의 성능을 극대화하는 것을 목표로 합니다.


## Usage
```bash
poetry install
poetry shell

# 반드시 datasets/articles.db 를 먼저 생성해야함
alembic upgrade head

# TASK1: 네이버 뉴스 링크 리스트를 datasets/articles.db 에 저장
scrapy crawl naver_news_content

# TASK2: 저장된 네이버 뉴스 링크 리스트에서 하나씩 뉴스 본문 파싱
scrapy crawl naver_news_list
```

## Scrapy-extension
- [scrapy-fake-agent](https://github.com/alecxe/scrapy-fake-useragent)
- [scrapy-playwright](https://github.com/scrapy-plugins/scrapy-playwright)

## html compression algorithm

The crawled HTML code is stored as binary, compressed using the `lzma` algorithm. [Simple tests](https://chat.openai.com/share/a0a256b4-6e04-4920-8f4e-7b7285977476) showed that among `lz4`, `gzip`, `bz2`, and `lzma`, `lzma` had the best compression ratio. Compression time was not considered.