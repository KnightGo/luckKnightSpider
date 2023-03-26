from cmath import log
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import re
class reiByListSpider(scrapy.Spider):
    name = 'roxy'
    allowed_domains = ['www.roxy.com']
    start_urls = ['https://www.roxy.com/sale/']
    def __init__(self, name=None, **kwargs):    
        self.fileName="roxy"

    def parse(self, response):
        try:
            print("》》》》》》》》",response.url) 
            products = response.css("div.r-tile-product-image a.omni_search_link")
            for product in products:
                yield response.follow(product, callback=self.parse_detail)

            if response.css("li.pagenext.disabled").get() is None:
                pto=response.css("li.pagenext a")
                yield from response.follow_all(pto, callback=self.parse)

        except Exception as e:
            print(e)

    def parse_detail(self, response):
        try:
            print("parse_detail:",response.url)
            product_verity=response.css("ul.r-swatchesdisplay-images li span::attr(data-href)")
            for product in product_verity:
                yield response.follow(product, callback=self.parse_vetiry_detail)

        except Exception as e:
                page = response.url.split("/")[-2]
                filename = f'{page}.html'
                with open(filename, 'wb') as f:
                    f.write(response.body)
                self.log(f'Saved file {filename}')
                print(e)


    def parse_vetiry_detail(self, response):
        try:
            print("---------------",response.url)
            detail_str =re.sub(r'\s+', ' ', ' '.join(response.xpath("//script[contains(text(), \"priceCurrency\")]").extract()))
            detail_json=re.findall(r'\{.+\}',str(detail_str))[0]
            detail_load = json.loads(detail_json)
            title=detail_load["name"]
            url=response.url
            image=detail_load["image"][-1]
            upc=detail_load["sku"]
            price=detail_load['offers']['price']
            original_price="-"
            inventory='-'

            if upc is not None:
                yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price='-',price=price,original_price=original_price,on_sale='-',inventory=inventory)

        except Exception as e:
                page = response.url.split("/")[-2]
                filename = f'{page}.html'
                with open(filename, 'wb') as f:
                    f.write(response.body)
                self.log(f'Saved file {filename}')
                print(e)
