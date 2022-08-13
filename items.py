# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LuckknightspiderItem(scrapy.Item):
    # define the fields for your item here like:
    image = scrapy.Field()
    url=scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field(serializer=str)
    price = scrapy.Field()
    size = scrapy.Field()
    color_name=scrapy.Field()
    inventory=scrapy.Field()
    original_price=scrapy.Field()
    on_sale=scrapy.Field()
    coupon_price=scrapy.Field()
    pass
