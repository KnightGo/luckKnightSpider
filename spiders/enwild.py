import json
import re
import scrapy

from ..items import LuckknightspiderItem

class EnwildSpider(scrapy.Spider):
    name = "enwild"
    allowed_domains = ["enwild.com"]
    start_urls = ["https://www.enwild.com/on-sale.html?Per_Page=-1&Sort_By=customfield_desc%3Acustomfields%3Asort_value"]
    def __init__(self, name=None, **kwargs):
        self.fileName="enwild"

    def parse(self, response):
        # Extract all product links on the page
        product_links = response.css("a.x-product-card__link::attr(href)").getall()

        for link in product_links:
            yield response.follow(link,callback=self.parse_product)

    def parse_product(self, response):
        try:
            product_script=response.xpath("//script[contains(text(), \"gtin\")]").extract()[0]
            json_script=json.loads(re.findall(r'\{.+\}',str(product_script))[0])['@graph'][0]
            if json_script.get('image') is not None:
                image=json_script['image']
            for variant in json_script['offers']:
                if variant.get('image') is not None:
                    image=variant['image']
                url=variant['url']
                title=variant['name']
                upc=variant['gtin']
                inventory='-'
                price=variant['price']
                original_price='-'
                on_sale='-'
                coupon_price='-'
                yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price=coupon_price,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)
        except Exception as e:
                print(response.url)
                print(e)