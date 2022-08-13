from cmath import log
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import re
from urllib import parse
class BelkTestSpider(scrapy.Spider):
    name = 'belktest'
    allowed_domains = ['belk.com']
    start_urls = ['https://www.belk.com/p/ontel-products-miracle-bamboo-pillow/9200775MBPFMC62.html']
    # def parse(self, response):
    #     yield from response.follow_all(css='sh-link::attr(href)', callback=self.parse_list)
    
    # def parse_list(self, response):
    #     try:
    #         print(response.url) 
    #         detail_info = response.css('ul.search-result-items script ').re(r'(?<=window.pageData.products = ).*?(?=;</script>)')[0]
    #         json_str_load = json.loads(detail_info)
    #         for item in json_str_load:
    #             print(item["url"])
    #             yield response.follow(item["url"], callback=self.parse_detail)

    #         yield from response.follow_all(css='a.page-next::attr(href)', callback=self.parse_list)
    #     except Exception as e:
    #         print(e)

    def parse(self, response):
        try:
            coupon_price=response.xpath("//span[contains(text(), \" after coupon\")]/preceding-sibling::span/text()").get()
            if coupon_price !=None:
                if coupon_price.__contains__('-'):
                    for url_item in response.xpath("//*[@id=\"va-size\"]/option/@value").extract():
                        if url_item != '' and url_item!=None and response.url!=url_item:
                            yield response.follow(url_item, callback=self.parse_one)
                else:
                    self.parse_one(self,response)
            else:
                self.parse_one(self,response)

        except Exception as e:
                page = response.url.split("/")[-2]
                filename = f'belk-{page}.html'
                with open('err_page\\'+filename, 'wb') as f:
                    f.write(response.body)
                self.log(f'Saved file {filename}')
                print(e)

        
    def parse_one(self,response):
        print(response.url)
        coupon_price=response.xpath("//span[contains(text(), \" after coupon\")]/preceding-sibling::span/text()").get()
        if coupon_price !=None:
            if coupon_price.__contains__('$'):
                coupon_price=coupon_price.replace('$','')
            else:
                coupon_price="0"
        else:
                coupon_price="0"
        utag_data_str =re.sub(r'\s+', ' ', ' '.join(response.xpath('//script[contains(text(), "sku_price")]').extract()))
        utag_data_json_str=re.findall(r'\{.+\}',utag_data_str)[0]
        utag_data_load = json.loads(utag_data_json_str)
        title=utag_data_load["product_name"][0]
        url= utag_data_load["product_url"][0]
        sku_inventory=utag_data_load["sku_inventory"] #库存数量集合
        sku_price=utag_data_load["sku_price"] #价格集合
        sku_original_price=utag_data_load["sku_original_price"] #原始价格集合
        sku_on_sale=utag_data_load["sku_on_sale"] #是否折扣
        sku_image_url=utag_data_load["sku_image_url"] #图片
        i=0
        for sku_upc in utag_data_load["sku_upc"]:#upc all
                upc=sku_upc
                inventory=sku_inventory[i]
                price=sku_price[i]
                original_price=sku_original_price[i]
                on_sale=sku_on_sale[i]
                image=sku_image_url[i]
                #if int(inventory)>=3 and float(price)/float(original_price)<=0.5:
                yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,coupon_price=coupon_price,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)
                i+=1