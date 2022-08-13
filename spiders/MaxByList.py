# -- coding: utf-8 --**
from cmath import log
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
from urllib import parse
import re
class MaxByListSpider(scrapy.Spider):
    name = 'maxbylist'
    allowed_domains = ['ih8i8h.a.searchspring.io']
    start_urls = [
        'https://www.maxwarehouse.com/collections/bird-feeding#/perpage:24'
        ]
    def parse(self, response):
        try:
            print(">>>>>>>>>>>>>>>>>>>>>>>>"+response.url) 
            collection=response.xpath('//script[contains(@hide-content, "#searchspring-content")]/@collection').get()
            script_searchspring=response.xpath('//script[contains(@hide-content, "#searchspring-content")]').get()
            searchspring=re.findall(r'(?<=[.]js[?]).*?(?=")',script_searchspring)[0]
            script_lastViewed=response.xpath('//script[contains(@hide-content, "#searchspring-content")]/following-sibling::script[1]/@src').get()
            lastViewed=re.findall(r'(?<=id=).*',script_lastViewed)[0]
            url="https://"+str(searchspring)+".a.searchspring.io/api/search/search.json?ajaxCatalog=v3&resultsFormat=native&siteId="+str(searchspring)+"&domain="+parse.quote(response.url,safe='')+"&bgfilter.collection_id="+str(collection)+"&resultsPerPage=72&q=&lastViewed="+str(lastViewed)+"&page=1"
            yield response.follow(url, callback=self.parse_detail)
        except Exception as e:
            print(response.url)
            print(e)
    
    def parse_detail(self, response):
        try:
            print(">>>>>>>>>>>>>>>>>>>>>>>>"+response.url) 
            body_json = json.loads(response.body)
            pagination=body_json["pagination"]
            nextPage=int(pagination["nextPage"])
            totalPages=int(pagination["totalPages"])
            currentPage=int(pagination["currentPage"])
            results=body_json["results"]
            for result in results:
                body_html=result["body_html"]
                image=result["image"]
                url=result["url"]
                title=result["name"]
                upc_re=re.search(r'(?<=UPC: ).\d*',body_html, re.M|re.I)
                if upc_re:
                    upc=upc_re.group()#"U_"+
                coupon_price="-"
                price=result["price"]
                original_price="-"
                on_sale="-"
                inventory="-"
               
                if price!=None and float(price) <= 200:
                    yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price=coupon_price,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)
            
            if currentPage!=totalPages:
                next_url=response.url.replace("page="+str(int(nextPage)-1),"page="+str(nextPage))
                print(">>>>>>>&&&&&&&&&&&&&&&&&&&"+next_url)
                yield scrapy.Request(url=next_url, callback=self.parse_detail)

        except Exception as e:
                print(response.url)
                print(e)


        



       