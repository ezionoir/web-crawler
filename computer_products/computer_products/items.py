# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ComputerProductsItem(scrapy.Item):
    # define the fields for your item here like:
    # retailer = scrapy.Field()
    # product_name = scrapy.Field()
    # product_brand = scrapy.Field()
    # product_price = scrapy.Field()
    # product_imglink = scrapy.Field()

    name = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    image = scrapy.Field()