# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ComputerProductsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    retailer = scrapy.Field()
    price = scrapy.Field()
    brand = scrapy.Field()
    url = scrapy.Field()
    img_url = scrapy.Field()