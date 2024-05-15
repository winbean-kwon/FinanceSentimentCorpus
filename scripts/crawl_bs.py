import csv
from bs4 import BeautifulSoup
import requests
import urllib
import time


base_url = 'https://n.news.naver.com/mnews/article'
header = {"user-agent": "Mozilla/5.0"}

companies = ['032','024','081','243','353','215','055','005','009','022','366','025','469','052','421','417','262','023','014','016','003','008','277','123','028','057','020','021','422','033','015','374','029','011','018','037','050','214']

with open('contents.csv', 'a', newline='', encoding="utf8") as to_write:
    writer = csv.writer(to_write)       

    for company in companies:
        for i in range(1, 10000000000):
            number = f'{i:010}' # 문자열 포멧팅
            url = base_url + '/' + company + '/' + number
            
            try:
                response = requests.get(url, headers=header, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('h2', class_="media_end_head_headline")

                    if title:
                        title_text = title.text.strip()
                    else:
                        title_text = "No title found"
                    print(f'URL: {url}, Title: {title_text}')
                    writer.writerow([url, title_text])

                else:
                    print(f'URL: {url}, Status Code: {response.status_code}')
                    break

            except requests.RequestException as e:
                print(f'Error for URL {url}: {str(e)}')
                time.sleep(10)
            time.sleep(1)



# news = soup.select("/html/body/div/div[2]/div")
