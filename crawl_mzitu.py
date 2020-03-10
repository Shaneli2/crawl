import requests
from lxml import etree
import random
import os


# 设计模式 --》面向对象编程
class Spider(object):
    def __init__(self, _dir="images"):
        self._dir = _dir
        self.browser = [
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
        ]
        # 反反爬虫措施，加请求头部信息
        self.headers = {
            'Origin': 'https://www.mzitu.com',
            'User-Agent': random.choice(self.browser),
            "Referer": "https://www.mzitu.com/xinggan/"
        }
        # save_path = os.path.join(os.path.abspath('.'),_dir)
        if not os.path.exists(os.path.join(os.path.abspath('.'), _dir)):
            os.mkdir(os.path.join(os.path.abspath('.'), _dir))

    def start_request(self):
        # 1. 获取整体网页的数据 requests
        for i in range(1, 242):  # 1 -242
            print("==========正在抓取%s页==========" % i)
            url = "https://www.mzitu.com/page/" + str(i) + "/"
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.content.decode())
            self.xpath_data(html)

    def xpath_data(self, html):
        # 2. 抽取想要的数据 标题 图片 xpath
        src_list = html.xpath('//ul[@id="pins"]/li/a/img/@data-original')
        alt_list = html.xpath('//ul[@id="pins"]/li/a/img/@alt')

        for src, alt in zip(src_list, alt_list):

            file_name = alt + ".jpg"
            response = requests.get(src, headers=self.headers)
            # print("正在抓取第 %d 张图片." % i)
            # 3. 存储数据 jpg with open
            try:
                with open(os.path.join(self._dir, file_name), "wb") as f:
                    f.write(response.content)


            except:
                print("==========文件名有误！==========")


spider = Spider()
spider.start_request()
print("Extraction done!")
