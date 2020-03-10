#! /usr/bin/env python3


from bs4 import BeautifulSoup
import requests
import csv
import time
import re
import random

csv_file = open('rent_lj3_newhouse.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file, delimiter=',')

browser = [
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
]

page = 1
url = 'https://gz.fang.lianjia.com/loupan/pg' + str(page) + '/#contentList'
headers = {
    'Origin': 'https://gz.fang.lianjia.com',
    'Referer': 'https://gz.fang.lianjia.com/loupan/pg2/',
    'User-Agent': random.choice(browser)
}

while True:
    time.sleep(2)
    res = requests.get(url, headers=headers)  # 抓取目标页面
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.find_all('div', class_='resblock-desc-wrapper')

    # 循环在读不到新的房源时结束
    if not items:
        break

    for item in items:
        title = item.find('div', class_='resblock-name').find('a').text
        type = item.find('span', class_='resblock-type').text
        saleStatus = item.find('span', class_='sale-status').text
        # district = add[0], street = add[1], addr=add[2]
        add = item.find('div', class_='resblock-location').text.split('/')
        room = item.find('a', class_='resblock-room').text.replace('\n',"").replace('/', ',')
        area = item.find('div', class_='resblock-area').find('span').text
        price1 = item.find('div', class_='main-price').text.replace('\n',"")
        if item.find('div', class_='second') is not None:
            price2 = item.find('div', class_='second').text
        other = item.find('div', class_='resblock-tag').text.replace('\n'," ")
        # add = re.findall('.*?·(.*?) .*', title)[0]
        #price = item.find('em').text
        link = 'https://gz.fang.lianjia.com' + item.find('div', class_='resblock-name').find('a')['href']
        writer.writerow([title, type, saleStatus,add[0].strip(),add[1].strip(),add[2].strip(),room,area,price1,price2,other,link])
        print("page %d of data extracted." % page)
    page += 1

csv_file.close()
