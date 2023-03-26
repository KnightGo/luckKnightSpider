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
class Acmetools(scrapy.Spider):
    name = 'acmetools'
    allowed_domains = ['acmetools.com']
    start_urls = ['https://www.acmetools.com/drill-accessories/']
    
    def __init__(self, name=None, **kwargs):
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        chrome_options =webdriver.ChromeOptions()# 使用headless无界面浏览器模式
        # chrome_options.add_argument('--headless') #增加无界面选项
        chrome_options.add_argument('--disable-gpu') 
        chrome_options.add_argument('--user-agent=%s'%user_agent)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', ])
        self.driver = webdriver.Chrome(executable_path=r'D:/ChromeDriver/106.0.5249.61/chromedriver.exe',options=chrome_options)
        
        self.fileName="acmetools"

        
    def parse(self, response):
        try:
            
            products = response.xpath('//*[@itemid="#product"]/div/div/div/div/a/@href').extract()
            for item in products:
                print(item)
                yield response.follow(item, callback=self.parse_detail)
                
            # print(pagedata["next_url"])
            # if pagedata["next_url"] is None:
            #         pagedata["next_url"]=response.url

            # yield response.follow(pagedata["next_url"], callback=self.parse)
        except Exception as e:
            print(e)


    def parse_detail(self, response):
        try:
            page = response.url.split("/")[-2]
            filename = f'{page}.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

        except Exception as e:
                print(response.url)
                print(e)