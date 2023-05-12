import scrapy
from ..items import ComputerProductsItem
import os

class GearVN_Spider(scrapy.Spider):
    name = 'GearVN'
    page_number = 1
    category_urls = {
        'laptop': [
            'https://gearvn.com/collections/laptop-hoc-tap-va-lam-viec-duoi-15tr',
            'https://gearvn.com/collections/laptop-hoc-tap-va-lam-viec-tu-15tr-den-20tr',
            'https://gearvn.com/collections/laptop-hoc-tap-va-lam-viec-tren-20-trieu',
            'https://gearvn.com/search?type=product&q=filter=((title%3Aproduct%20adjacent%20laptop%20gaming))'
        ],

    }
    start_urls = [
        'https://gearvn.com/'
    ]
    custom_settings = {
        'FEED_URI': 'crawl_results/gearvn.json',
        'FEED_FORMAT': 'json'
    }

    def __init__(self, category=None, *args, **kwargs):
        super(GearVN_Spider, self).__init__(*args, **kwargs)
        if category is not None:
            self.start_urls = self.category_urls.get(category, None)

    def parse(self, response):
        if response.status == 200:
            tokens = response.css('div.product-row')
            if len(tokens) <= 0:
                return None

            items = ComputerProductsItem()

            for token in tokens:
                items['name'] = token.css('h2::text').extract()[0]
                items['retailer'] = 'GearVN'
                items['price'] = token.css('div.product-row-info div span::text').extract()[0]
                items['brand'] = 'unknown'
                items['url'] = 'https://gearvn.com' + token.css('a::attr(href)').extract()[0]
                items['img_url'] = 'http://gearvn.com' + token.css('div.product-row-img img::attr(src)').extract()[0]

                yield items

            self.page_number += 1
            next_page = self.start_urls[0] + f'&page={self.page_number}'

            yield response.follow(next_page, callback=self.parse)