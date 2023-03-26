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

class BelkSearchByListSpider(scrapy.Spider):
    name = 'belkbylistsearch'
    allowed_domains = ['belk.com']
    start_urls = ['https://www.belk.com/search/?prefn1=groupedEventCodeID&prefv1=22BFSDB&start=10080&sz=60']
    def __init__(self, name=None, **kwargs):
        chrome_options =webdriver.ChromeOptions()# 使用headless无界面浏览器模式
        chrome_options.add_argument('--headless') #增加无界面选项
        chrome_options.add_argument('--disable-gpu') 
        self.driver = webdriver.Chrome(executable_path=r'D:/ChromeDriver/106.0.5249.61/chromedriver.exe',options=chrome_options)
        
        self.fileName="belk_coupon"

    def parse(self, response):
        try:
            pagedata = json.loads(response.body)
            products=json.loads(pagedata["page_data"])
            for item in products:
                print(item["url"])
                yield response.follow(item["url"], callback=self.parse_detail)
                
            print(pagedata["next_url"])
            if pagedata["next_url"] is None:
                    pagedata["next_url"]=response.url

            yield response.follow(pagedata["next_url"], callback=self.parse)
        except Exception as e:
            print(e)

    def parse_detail(self, response):
        try:
            utag_data_str =re.sub(r'\s+', ' ', ' '.join(response.xpath('//script[contains(text(), "sku_price")]').extract()))
            if utag_data_str !='':
                utag_data_json_str=re.findall(r'\{.+\}',utag_data_str)[0]
                utag_data_load = json.loads(utag_data_json_str)
                title=utag_data_load["product_name"][0]
                url= utag_data_load["product_url"][0]
                sku_inventory=utag_data_load["sku_inventory"] #库存数量集合
                sku_price=utag_data_load["sku_price"] #价格集合
                sku_original_price=utag_data_load["sku_original_price"] #原始价格集合
                sku_on_sale=utag_data_load["sku_on_sale"] #是否折扣
                sku_image_url=utag_data_load["sku_image_url"] #图片
                coupon_price=response.xpath("//span[contains(text(), \" after coupon\")]/preceding-sibling::span/text()").get()
                if coupon_price !=None:
                    coupon_price=coupon_price.replace('$','')
                else:
                    coupon_price="0"

                i=0
                for sku_upc in utag_data_load["sku_upc"]:#upc all
                    upc=sku_upc
                    inventory=sku_inventory[i]
                    price=sku_price[i]
                    original_price=sku_original_price[i]
                    on_sale=sku_on_sale[i]
                    image=sku_image_url[i]
                    if int(inventory)>=3:
                      yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price=coupon_price,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)
                    i+=1
            # else:
            #     upc=response.css('span.product-UPC::text').get()
            #     if upc !=None:
            #         upc=upc.replace('UPC: ','')
            #         title=response.css("div.brand-name::text").get()
            #         detail_url=response.css('ul.swatches li div::attr("data-href")').getall()
            #         standardprice=response.css('span.standardprice::text').get()
            #         standardprice_span=response.css('span.standardprice span').get()
            #         price=standardprice.replace(standardprice_span,'').replace('$','')
            #         coupon_price=response.xpath('//div[@class="vjs_price-with-coupon"]//span[contains(text(), "$")]/text()').get()
            #         if coupon_price!=None:
            #             coupon_price=coupon_price.replace('$','')
            #         img = re.sub(r'\s+', ' ', ' '.join(response.xpath('//script[@id="colorSizeMapping"]/text()').extract()))
            #         img_json_str=re.findall(r'\{.+\}',img)[0]
            #         img_json_load = json.loads(img_json_str)
            #         WANNYTAH9_color=re.findall(r'\WANNYTAH9_color.+\&',detail_url)[0].replace('WANNYTAH9_color=','').replace('&','')
            #         image=img_json_load["colors"][WANNYTAH9_color]["imgUrl"]
            #         original_price="-"
            #         on_sale="-"
            #         inventory="-"
            #         yield LuckknightspiderItem(image=image,url=detail_url,title=title,upc=upc,coupon_price=coupon_price,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)


        except Exception as e:
                # page = response.url.split("/")[-2]
                # filename = f'belk-{page}.html'
                # with open('err_page\\'+filename, 'wb') as f:
                #     f.write(response.body)
                # self.log(f'Saved file {filename}')
                print(response.url)
                print(e)