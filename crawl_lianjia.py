#! /usr/bin/env python3


from bs4 import BeautifulSoup
import requests
import csv
import time
import re
import random

csv_file = open('rent_lj3.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file, delimiter=',')

browser = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
]

page = 1
url = 'https://gz.lianjia.com/ditiezufang/pg' + str(page) + '/#contentList'
headers = {
    'Origin': 'https://gz.lianjia.com',
    'Referer': 'https://gz.lianjia.com/ditiezufang/pg2/',
    'User-Agent': random.choice(browser)
}

while page <= 10:
    time.sleep(2)
    res = requests.get(url, headers=headers)  # 抓取目标页面
    print(res.status_code)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='content__list--item--main')
    for item in items:
        title = item.find('p', class_='content__list--item--title twoline').find('a').text
        if '青年公寓' in title:
            continue
        add = re.findall('.*?·(.*?) .*', title)[0]
        price = item.find('em').text
        link = 'https://gz.lianjia.com' + item.find('p', class_='content__list--item--title twoline').find('a')['href']
        writer.writerow([title.lstrip(), add, price, link])
    page += 1

csv_file.close()
