# -- coding: utf-8 --**
from cmath import log
from operator import truediv
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import re
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from scrapy.http.response.html import HtmlResponse
import json
from selenium.webdriver.common.by import By
#未完成
class Planetcyclery(scrapy.Spider):
    name = 'planetcyclery'
    allowed_domains = ['planetcyclery.com']
    start_urls = ['https://planetcyclery.com/sale/clearance']
    
    def __init__(self, name=None, **kwargs):
        self.cookies = {
        "name": "cf_chl_2",
        "value": "dbf75f29ae317e6",
        "name": "cf_clearance",
        "value": "8kdAxZ3VC_HkogbOiftfkCtOP4Cn.29osxNXcgv7uY0-1669442323-0-250",
        "name": "PHPSESSID",
        "value": "fiquivi482et88ldjij1paqep1",
        "name": "_gcl_au",
        "value": "1.1.1879508771.1669442329",
        "name": "zaius_js_version",
        "value": "2.21.4",
        "name": "z_idsyncs",
        "value": "",
        "name": "vtsrc",
        "value": "source%3Ddirect%7Cmedium%3Dnone",
        "name": "_ga",
        "value": "GA1.2.1909740553.1669442331",
        "name": "_gid",
        "value": "GA1.2.464821593.1669442331",
        "name": "klv_mage",
        "value": "{\"expire_sections\":{\"customerData\":1669442935}}",
        "name": "_fbp",
        "value": "fb.1.1669442335354.228372335",
        "name": "vuid",
        "value": "f486df68-b404-46aa-99a7-f16668d27149%7C1669442335410",
        "name": "_uetsid",
        "value": "66f369e06d4f11ed81e449a890ec0fbe",
        "name": "_uetvid",
        "value": "66f38a106d4f11ed9e50953081ac5579",
        "name": "form_key",
        "value": "5mG7vBVhGX1DaEtx",
        "name": "mage-cache-storage",
        "value": "%7B%7D",
        "name": "mage-cache-storage-section-invalidation",
        "value": "%7B%7D",
        "name": "mage-cache-sessid",
        "value": "true",
        "name": "mage-messages",
        "value": "",
        "name": "recently_viewed_product",
        "value": "%7B%7D",
        "name": "recently_viewed_product_previous",
        "value": "%7B%7D",
        "name": "recently_compared_product",
        "value": "%7B%7D",
        "name": "recently_compared_product_previous",
        "value": "%7B%7D",
        "name": "product_data_storage",
        "value": "%7B%7D"
    }

        chrome_options =webdriver.ChromeOptions()# 使用headless无界面浏览器模式
        # chrome_options.add_argument('--headless') #增加无界面选项
        chrome_options.add_argument('--disable-infobars') # 禁止策略化
        chrome_options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('window-size=1920x3000') # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--incognito') # 隐身模式（无痕模式）
        chrome_options.add_argument('--disable-javascript') # 禁用javascript
        chrome_options.add_argument('--start-maximized') # 最大化运行（全屏窗口）,不设置，取元素会报错
        chrome_options.add_argument('--disable-infobars') # 禁用浏览器正在被自动化程序控制的提示
        chrome_options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
        #chrome_options.add_argument('blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
        chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"')
        chrome_options.add_argument('Accept-Language="zh,zh-CN;q=0.9,en;q=0.8"')

        
        self.driver = webdriver.Chrome(executable_path=r'D:/ChromeDriver/106.0.5249.61/chromedriver.exe',options=chrome_options)
        self.fileName="planetcyclery"

        
    def parse(self, response):
        try:
            page = response.url.split("/")[-2]
            filename = f'{page}.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

            # products = response.xpath('//*[@itemid="#product"]/div/div/div/div/a/@href').extract()
            # for item in products:
            #     print(item)
            #     yield response.follow(item, callback=self.parse_detail)
                
            # print(pagedata["next_url"])
            # if pagedata["next_url"] is None:
            #         pagedata["next_url"]=response.url

            # yield response.follow(pagedata["next_url"], callback=self.parse)
        except Exception as e:
            print(e)


    # def parse_detail(self, response):
    #     try:
    #         page = response.url.split("/")[-2]
    #         filename = f'{page}.html'
    #         with open(filename, 'wb') as f:
    #             f.write(response.body)
    #         self.log(f'Saved file {filename}')

    #     except Exception as e:
    #             print(response.url)
    #             print(e)