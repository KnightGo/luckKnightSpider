# -- coding: utf-8 --**
from cmath import log
import scrapy
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import json
class BikeclosetSpider(scrapy.Spider):
    name = 'bikecloset'
    allowed_domains = ['bikecloset.com']
    start_urls = [
        'https://bikecloset.com/product-category/accessories/lights/',
        'https://bikecloset.com/product-category/accessories/pedals/',
        'https://bikecloset.com/product-category/optics/',
        'https://bikecloset.com/product-category/accessories/tires/',
        'https://bikecloset.com/product-category/accessories/helmets/',
        'https://bikecloset.com/product-category/clothing/',
        'https://bikecloset.com/product-category/builders-corner/',
        'https://bikecloset.com/product-category/bags-packs/',
        'https://bikecloset.com/product-category/accessories/tools/',
        'https://bikecloset.com/product-category/im-cheap/'
        ]
    def __init__(self, name=None, **kwargs):
        self.fileName="bikecloset"
    def parse(self, response):
        try:
             #TODO:
                # 列表页!=Out of stock 需要随机等待 开启配置：DOWNLOAD_DELAY=2 RANDOMIZE_DOWNLOAD_DELAY=True
                #1、判断=Add to cart  查询当前商品块 地址、图片、价格、等信息返回 √
                #2、判断=Select options 进入详情页获取变体信息
            print(">>>>>>>>>>>>>>>>>>>>>>>>"+response.url) 
            product_list=response.css('div.content-product')
            for product_block in product_list:
               isStock=product_block.css('p.stock::text').get()
               if isStock!="Out of stock":
                 toCart=product_block.css('a.add_to_cart_button::text').get()
                 if toCart=="Add to cart":
                        title=product_block.css('p.product-title a::text').get()
                        url=product_block.css('p.product-title a::attr(href)').get()
                        coupon_price=product_block.css('span.price ins bdi::text').get()
                        if coupon_price is None:
                            coupon_price=product_block.css("span.price bdi::text").get()

                        image=product_block.css('a.product-content-image img::attr(data-src)').get()
                        upc=product_block.css('a.add_to_cart_button::attr(data-product_sku)').get()
                        yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price=coupon_price,price="-",original_price="-",on_sale="-",inventory="-")
                 else:
                     if toCart=="Select options":
                        detail_url=product_block.css('p.product-title a::attr(href)').get()
                        yield response.follow(detail_url, callback=self.parse_detail)
                        


                    
        except Exception as e:
            print(response.url)
            print(e)
    
   
    def parse_detail(self, response):
        try:
            print(">>>>>>>>>>>>>>>>>>>>>>>>"+response.url) 
            json_str=response.css('form.variations_form::attr(data-product_variations)').get()
            body_json = json.loads(json_str)
            for product_block in body_json:
                if product_block["availability_html"].__contains__("In stock"):
                    title=product_block["image"]["title"]
                    url=response.url
                    coupon_price=product_block["display_price"]
                    image=product_block["image"]["src"]
                    upc=product_block["sku"]
                    yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price=coupon_price,price="-",original_price="-",on_sale="-",inventory="-")

        except Exception as e:
                print(response.url)
                print(e)


        



       