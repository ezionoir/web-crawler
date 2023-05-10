import scrapy
from ..items import ComputerProductsItem
import os
import sys

class PhongVu_Spider(scrapy.Spider):
    name = 'PhongVu'
    page_number = 1
    start_urls = [
        'https://phongvu.vn/'
    ]
    custom_settings = {
        'FEED_URI': 'phongvu.json',
        'FEED_FORMAT': 'json'
    }

    def __init__(self, query=None, category=None, *args, **kwargs):
        super(PhongVu_Spider, self).__init__(*args, **kwargs)
        if query is not None:
            self.start_urls = [
                f'https://phongvu.vn/search?router=productListing&query={query}'
            ]

    def parse(self, response):
        if response.status == 200:
            tokens = response.css('div.css-4rhdrh')
            if len(tokens) <= 0:
                return None

            items = ComputerProductsItem()

            for token in tokens:
                items['name'] = token.css('div.css-1ybkowq div h3::text').extract()[0]
                items['price'] = token.css('div.css-kgkvir > div.css-1co26wt > div::text').extract()
                if len(items['price']) > 1:
                    separator = ''
                    price = separator.join(items['price'])
                    items['price'] = price
                else:
                    items['price'] = items['price'][0]

                items['brand'] = token.css('div.css-68cx5s div::text').extract()[0]
                items['url'] = token.css('div.css-1v97aik div div img::attr(src)').extract()[0]
                items['image'] = token.css('div.css-1v97aik div div img::attr(src)').extract()[0]

                yield items

            self.page_number += 1
            next_page = self.start_urls[0] + f'&page={self.page_number}'
            yield response.follow(next_page, callback=self.parse)