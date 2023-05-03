import json
import scrapy
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
from urllib.parse import urljoin,urlparse
import re

class CampSaverSpider(scrapy.Spider):
    name = "campsaver"
    allowed_domains = ["campsaver.com"]
    start_urls = ["https://www.campsaver.com/outlet.html?_iv_gridSize=240"]
    global index
    def __init__(self, name=None, **kwargs): 
        self.fileName="campsaver"
        
    def parse(self, response):
        
        # Extract all product items on the page
        product_links = response.css("div.grid-c__main div a::attr(href)").getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product_details)
        
        index = 2
        while index < 11:
           yield response.follow("https://www.campsaver.com/outlet.html?_iv_page="+str(index)+"&_iv_gridSize=240", callback=self.parse)
           index+=1

    def parse_product_details(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>>>>"+response.url)
        url=urljoin(response.url,urlparse(response.url).path)
        detail_str = response.xpath("//script[contains(text(), '"+str(url)+"')]").get()
        detail_json=re.findall(r'\{.+\}',str(detail_str))[0]
        detail_load = json.loads(detail_json)    

        image_url = detail_load["image"]
        title = detail_load["name"]

        for item in detail_load["offers"]:
            sku = item["gtin13"]
            discount_price = item["price"]
            address = response.url
            # Yield a dictionary containing the extracted data for the requested product
            yield LuckknightspiderItem(image=image_url,url=address,title=title,upc=sku,coupon_price=discount_price,price='-',original_price="-",on_sale='-',inventory='-')
