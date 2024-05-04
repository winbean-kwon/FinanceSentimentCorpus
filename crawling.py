import csv
from bs4 import BeautifulSoup
import requests
import urllib
import time


base_url = 'https://n.news.naver.com/mnews/article'
header = {"user-agent": "Mozilla/5.0"}

companies = ['032', '024', '081', '243', '353', '215', '055', '005', '009', '022', '366', '025', '469', '052', '421', '417', '262', '023', '014', '016', '003', '008', '277', '123', '028', '057', '020', '021', '422', '033', '015', '374', '029', '011', '018', '037', '050', '214']
          
for company in companies:
     for i in range(1, 10000000000):
        number = f'{i:010}' # 문자열 포멧팅
        url = base_url + '/' + company + '/' + number
        html = requests.get(url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        try:
            response = requests.get(url, timeout=5)
            print(f'URL: {url}, Status Code: {response.status_code}')
            title = soup.find('h2', "media_end_head_headline")
            print(title)
            with open('contents.csv', 'a', newline='', encoding="utf8") as to_write:
                writer = csv.writer(to_write)
                writer.writerow([title])
            
            if response.status_code != 200:
                break
        except requests.RequestException as e:
            print(f'Error for URL {url}: {str(e)}')
            time.sleep(10)
        time.sleep(1)


# news = soup.select("/html/body/div/div[2]/div")
