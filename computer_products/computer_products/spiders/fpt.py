import scrapy
from ..items import ComputerProductsItem

class FPT_Spider(scrapy.Spider):
    name = 'FPT'
    page_number = 1
    start_urls = [
        'https://fptshop.com.vn'
    ]

    def __init__(self, query=None, *args, **kwargs):
        super(FPT_Spider, self).__init__(*args, **kwargs)
        if query is not None:
            self.start_urls = [
                f'https://fptshop.com.vn/tim-kiem/{query}'
            ]

    def parse(self, response):
        if response.status == 200:

            scrapy.utils.response.open_in_browser(response)

            tokens = response.css('div.cdt-product')
            if len(tokens) <= 0:
                return None


            items = ComputerProductsItem()

            for token in tokens:
                items['retailer'] = 'Phong Vu'
                items['product_name'] = token.css('div.cdt-product__info h3 a::attr(title)').extract()
                items['product_brand'] = ['Unknown']
                items['product_price'] = token.css('div.cdt-product__info div.cdt-product__show-promo div.progress').extract()
                if len(items['product_price']) > 1:
                    separator = ''
                    price = separator.join(items['product_price'])
                    items['product_price'] = [price]

                items['product_imglink'] = token.css('div.cdt-product__img a::attr(href)').extract()

                yield items

            # self.page_number += 1
            # next_page = self.start_urls[0] + f'&page={self.page_number}'
            # yield response.follow(next_page, callback=self.parse)