import scrapy
from ..items import ComputerProductsItem
import os

class HaNoiComputer_Spider(scrapy.Spider):
    name = 'HaCom'
    page_number = 1
    start_urls = [
        'https://hacom.vn'
    ]
    custom_settings = {
        'FEED_URI': 'crawl_results/hacom.json',
        'FEED_FORMAT': 'json'
    }

    def __init__(self, query=None, *args, **kwargs):
        super(HaNoiComputer_Spider, self).__init__(*args, **kwargs)
        if query is not None:
            self.start_urls = [
                f'https://hacom.vn/tim?q={query}'
            ]

    def parse(self, response):
        if response.status == 200:
            tokens = response.css('div.p-component')
            if len(tokens) <= 0:
                return None

            items = ComputerProductsItem()

            for token in tokens:
                items['name'] = token.css('div.p-info h3 a::text').extract()[0]
                items['retailer'] = 'Hanoicomputer'
                items['price'] = token.css('div.p-info span.p-price::attr(data-price)').extract()[0]
                items['brand'] = 'unknown'
                items['url'] = 'https://hacom.vn' + token.css('div.p-img a::attr(href)').extract()[0]
                items['img_url'] = token.css('div.p-img a img::attr(data-src)').extract()[0]

                yield items

            self.page_number += 1
            next_page = self.start_urls[0] + f'&page={self.page_number}'
            yield response.follow(next_page, callback=self.parse)