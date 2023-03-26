# -- coding: utf-8 --**
from cmath import log
from operator import truediv
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import re
import json
class Harrisweldingsupplies(scrapy.Spider):
    name = 'harrisweldingsupplies'
    allowed_domains = ['harrisweldingsupplies.com']
    start_urls = ['https://www.harrisweldingsupplies.com/welding-accessories/']
    def __init__(self, name=None, **kwargs):
        self.fileName="harrisweldingsupplies"
    def parse(self, response):
        try:
            print(">>>>>>>>>>>>>>>",response.url)
            products=response.css('ul.productGrid li a.card-figure__link')
            for product in products:
                yield response.follow(product, callback=self.parse_detail)
            pto=response.css("li.pagination-item--next a")
            yield from response.follow_all(pto, callback=self.parse) 
        except Exception as e:
            print(e)

    def parse_detail(self, response):
        try:
            print("---------------",response.url)
            detail_str =re.sub(r'\s+', ' ', ' '.join(response.xpath("//script[contains(text(), \"BCData\")]").extract()))
            detail_json=re.findall(r'\{.+\}',str(detail_str))[0]
            detail_load = json.loads(detail_json)["product_attributes"]
            title=response.css('h1.productView-title::text').get()
            url= response.url
            image=response.css('div.productView-img-container a::attr(href)').get()
            upc=detail_load["upc"]
            inventory='-'
            price=detail_load['price']['without_tax']['value']
            if 'rrp_without_tax' in detail_json:
                original_price=detail_load['price']['rrp_without_tax']['value']
            else:
                original_price=price
            if upc is not None:
                yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price='-',price=price,original_price=original_price,on_sale='-',inventory=inventory)

        except Exception as e:
                page = response.url.split("/")[-2]
                filename = f'{page}.html'
                with open(filename, 'wb') as f:
                    f.write(response.body)
                self.log(f'Saved file {filename}')
                print(e)
