import scrapy
from ..items import ComputerProductsItem
import os
import sys

class PhongVu_Spider(scrapy.Spider):
    name = 'PhongVu'
    page_number = 1
    category_urls = {
        'laptop': 'https://phongvu.vn/c/laptop',
        'mobile': 'https://phongvu.vn/c/phone-dien-thoai',
        'tablet': 'https://phongvu.vn/c/may-tinh-bang'
    }
    start_urls = [
        'https://phongvu.vn/'
    ]
    custom_settings = {
        'FEED_URI': 'crawl_results/phongvu.json',
        'FEED_FORMAT': 'json'
    }

    def __init__(self, category=None, *args, **kwargs):
        super(PhongVu_Spider, self).__init__(*args, **kwargs)
        if category is not None:
            self.start_urls = [self.category_urls.get(category, None)]

    def parse(self, response):
        if response.status == 200:
            tokens = response.css('div.product-card')
            if len(tokens) <= 0:
                return None

            items = ComputerProductsItem()

            for token in tokens:
                items['name'] = token.css('div.css-1ybkowq div h3::text').extract()[0]
                items['retailer'] = 'Phong Vu'
                items['price'] = token.css('div.css-kgkvir > div.css-1co26wt > div::text').extract()
                if len(items['price']) > 1:
                    separator = ''
                    price = separator.join(items['price'])
                    items['price'] = price
                else:
                    items['price'] = items['price'][0]

                items['brand'] = token.css('div.css-68cx5s div::text').extract()[0]
                items['url'] = 'https://phongvu.vn/' + token.css('a.css-pxdb0j::attr(href)').extract()[0]
                items['img_url'] = token.css('div.css-1v97aik div div img::attr(src)').extract()[0]

                yield items

            self.page_number += 1
            next_page = self.start_urls[0] + f'&page={self.page_number}'
            yield response.follow(next_page, callback=self.parse)