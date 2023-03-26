import scrapy
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入

class ToyshnipSpider(scrapy.Spider):
    name = "toyshnip"
    allowed_domains = ["toyshnip.com"]
    start_urls = ["https://toyshnip.com/pages/collections-by-manufacturer"]

    def __init__(self, name=None, **kwargs): 
        self.fileName="toyshnip"

    def parse(self, response):
        # Extract links to collection pages
        collection_links = response.css("div.rte--nomargin a::attr(href)").getall()
        for link in collection_links:
            yield response.follow(link, callback=self.parse_collection_page)

    def parse_collection_page(self, response):
        print(">>>>>>>>>>>>>>>>>>>>>>>>"+response.url) 
        # Extract links to product pages
        product_links = response.css("div.medium-up--four-fifths a.grid-item__link::attr(href)").getall()
        for link in product_links:
            yield response.follow(link, callback=self.parse_product_page)
        
        # Follow pagination links
        next_page_link = response.css("span.next a.btn::attr(href)").get()
        if next_page_link:
            yield response.follow(next_page_link, callback=self.parse_collection_page)

    def parse_product_page(self, response):
        # Extract SKU, original price, discount price, product image address, product address, and title from the product page
        sku = response.xpath("(//span[@class='product-single__sku']/span[1])[2]/text()").get()
        original_price = response.xpath("//span[@class='product__price product__price--compare']/span[1]/span/text()").get()
        if original_price==None:
            original_price = response.xpath("//span[@class='product__price']/span[1]/span/text()").get()

        if original_price!=None:
            original_price=original_price.replace('$','').replace(' USD','')

        discount_price = response.xpath("//span[@class='product__price on-sale']/span[1]/span/text()").get()

        if discount_price!=None:
            discount_price=discount_price.replace('$','').replace(' USD','')

        image_url = response.css("img.photoswipe__image::attr(data-photoswipe-src)").get() 
        if image_url!=None:
            image_url="https:"+image_url

        address = response.url
        title = response.css("h1.product-single__title::text").get()
        yield LuckknightspiderItem(image=image_url,url=address,title=title,upc=sku,coupon_price=discount_price,price='-',original_price=original_price,on_sale='-',inventory='-')