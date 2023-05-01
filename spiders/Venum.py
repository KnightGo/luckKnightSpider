# -- coding: utf-8 --**
from cmath import log
from operator import truediv
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import re
import json
class VenumSpider(scrapy.Spider):
    name = 'venum'
    allowed_domains = ['venum.com']
    start_urls = ['https://www.venum.com/collections/sales']
    def __init__(self, name=None, **kwargs):
        self.fileName="venum"
        self.total_page=13


    def parse(self, response):
        #use scrapy crawl https://api.fastsimon.com/categories_navigation?request_source=v-next&src=v-next&UUID=8c926b80-91c6-4d5e-b7b7-715a07ae6398&uuid=8c926b80-91c6-4d5e-b7b7-715a07ae6398&store_id=26422181937&api_type=json&category_id=262609633541&facets_required=1&products_per_page=20&page_num=10&with_product_attributes=true&sp=6669941342469, and then crawl each product link,image,price,description,title
        autocomplete_initilizer=response.xpath('//*[@id="autocomplete-initilizer"]/@src').extract()
        uuid=''
        store_id=''
        # page_num=1
        category_id=re.findall(r'\".+\"',response.xpath('//script[contains(text(), "CATEGORY_ID")]/text()').extract()[0])[0].replace('"','')
        autocomplete_initilizer=autocomplete_initilizer[0]
        for item in autocomplete_initilizer.split('&'):
                if '=' in item:
                    key=item.split('=')[0]
                    value=item.split('=')[1]
                    if key=='UUID':
                        uuid=value
                    if key=='store':
                        store_id=value
        
        if uuid!='' and store_id!='':
            for page_num in range(1,13):
                url='https://api.fastsimon.com/categories_navigation?request_source=v-next&src=v-next&UUID='+uuid+'&uuid='+uuid+'&store_id='+store_id+'&api_type=json&category_id='+category_id+'&facets_required=1&products_per_page=50&page_num='+str(page_num)+'&with_product_attributes=true&sp=6669941342469'
                yield scrapy.Request(url=url, callback=self.parse_product,dont_filter=True)
                #yield response.follow(url, callback=self.parse_product)
                print(page_num)

            
    
    def parse_product(self,response): 
            print("parse_product>>>>>>>>>>>"+response.url)
            body = json.loads(response.body)
            self.total_page = body['total_p']
            items = body['items']
            for item in items:
                product_url='https://www.venum.com'+item['u']+'.json'
                yield scrapy.Request(url=product_url, callback=self.parse_product_detail)
                #yield response.follow(product_url, callback=self.parse_product_detail)

    def parse_product_detail(self,response):
        print("parse_product_detail>>>>>>>>>>>"+response.url)
        body = json.loads(response.body)
        product = body['product']
        
        title=product['title']
        image=product['image']['src']
        variants = product['variants']
        for variant in variants:
            upc=variant['barcode']
            inventory='-'
            price=variant['price']
            original_price=variant['compare_at_price']
            on_sale='-'
            coupon_price='-'
            yield LuckknightspiderItem(image=image,url=response.url,title=title,upc=upc,coupon_price=coupon_price,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)

                

        




            
            


        

   