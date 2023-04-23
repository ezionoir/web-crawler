import scrapy
from ..items import ComputerProductsItem

class GearVN_Spider(scrapy.Spider):
    name = 'GearVN'
    page_number = 1
    start_urls = [
        'https://gearvn.com/'
    ]

    def __init__(self, query=None, *args, **kwargs):
        super(GearVN_Spider, self).__init__(*args, **kwargs)
        if query is not None:
            self.start_urls = [
                f'https://gearvn.com/search?type=product&q=filter=((title%3Aproduct%20adjacent%20{query}))'
            ]

    def parse(self, response):
        if response.status == 200:
            tokens = response.css('div.product-row')
            if len(tokens) <= 0:
                return None

            items = ComputerProductsItem()

            for token in tokens:
                items['retailer'] = 'GearVN'
                items['product_name'] = token.css('h2::text').extract()
                items['product_brand'] = ['Unknown']
                items['product_price'] = token.css('div.product-row-info div span::text').extract()
                items['product_imglink'] = token.css('div.product-row-img img::attr(src)').extract()

                yield items

            self.page_number += 1
            next_page = self.start_urls[0] + f'&page={self.page_number}'

            yield response.follow(next_page, callback=self.parse)