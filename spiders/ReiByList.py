from cmath import log
import scrapy
import json
from ..items import LuckknightspiderItem  # 从上一层的items.py文件里导入
import re
class reiByListSpider(scrapy.Spider):
    name = 'reibylist'
    allowed_domains = ['www.rei.com']
    start_urls = ['https://www.rei.com/f/scd-deals']
    def parse(self, response):
        try:
            print(response.url) 
            list_str = re.sub(r'\s+', ' ', ' '.join(response.xpath("//*[@id=\"initial-props\"]").extract()))
            list_json=re.findall(r'\{.+\}',str(list_str))[0]
            list_json_load = json.loads(list_json)
            for item in list_json_load["ProductSearch"]["products"]["searchResults"]["results"]:
                # print(item["link"])
                yield response.follow(item["link"], callback=self.parse_detail)
            pto=response.xpath("//span[contains(text(), \"Go to next page\")]/parent::a/@href").extract()
            yield from response.follow_all(pto, callback=self.parse) #pto
        except Exception as e:
            print(e)

    def parse_detail(self, response):
        try:
            detail_str =re.sub(r'\s+', ' ', ' '.join(response.xpath("//*[@id=\"modelData\"]").extract()))
            if detail_str != '' :
                detail_json=re.findall(r'\{.+\}',str(detail_str))[0]
                detail_load = json.loads(detail_json)
                title=detail_load["title"]
                url= detail_load["openGraphProperties"]["og:url"]
                image_url_host=detail_load["openGraphProperties"]["og:image"].replace('product','color')
                bySku=detail_load["pageData"]["product"]["bySku"] #图片
                i=0
                for sku_upc in detail_load["pageData"]["product"]["skus"]:#upc all
                    if sku_upc["upc"] != None and sku_upc["status"] == "AVAILABLE":
                        upc="U_"+sku_upc["upc"]
                        inventory=0
                        price=sku_upc["price"]["price"]["value"]
                        original_price=sku_upc["price"]["price"]["compValue"]
                        on_sale=float(price)/float(original_price)<=0.5
                        image=image_url_host+"?colorId="+bySku[sku_upc["skuId"]]["color"]["code"]
                        if float(original_price)!=0 and float(price)/float(original_price)<=0.5:
                            yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)
                        i+=1
            else:
                detail_str =re.sub(r'\s+', ' ', ' '.join(response.xpath("//*[@id=\"page-data\"]").extract()))
                if detail_str != '' :
                    detail_json=re.findall(r'\{.+\}',str(detail_str))[0]
                    detail_load = json.loads(detail_json)["product"]
                    title=detail_load["title"]
                    url= "https://www.rei.com" + detail_load["canonical"]
                    media=detail_load["media"] #图片信息合集
                    img_dic = {"1":"0"}
                    for media_item in media:
                        img_dic.setdefault(media_item["sku"],media_item["link"])                                
                    for sku_upc in detail_load["variants"]: #upc all
                        if sku_upc["identifiers"][0]["type"] == "UPC" and sku_upc["status"] == "AVAILABLE":
                            upc="U_"+sku_upc["identifiers"][0]["value"]
                            inventory=sku_upc["quantity"]
                            price=sku_upc["price"]
                            original_price=sku_upc["compareAtPrice"]
                            on_sale=float(price)/float(original_price)<=0.5
                            image="https://www.rei.com/" + img_dic.get(sku_upc["sku"],"not image")

                            if float(original_price)!=0 and float(price)/float(original_price)<=0.5:
                                yield LuckknightspiderItem(image=image,url=url,title=title,upc=upc,price=price,original_price=original_price,on_sale=on_sale,inventory=inventory)

        except Exception as e:
                page = response.url.split("/")[-2]
                filename = f'rei-{page}.html'
                with open('err_page\\'+filename, 'wb') as f:
                    f.write(response.body)
                self.log(f'Saved file {filename}')
                print(e)

        



       