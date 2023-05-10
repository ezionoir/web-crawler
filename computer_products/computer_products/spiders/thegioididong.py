import scrapy
from ..items import ComputerProductsItem

class TGDD_Spider(scrapy.Spider):
    name = 'TheGioiDiDong'
    page_number = 1
    start_urls = [
        'https://www.thegioididong.com/'
    ]

    def __init__(self, query=None, *args, **kwargs):
        super(TGDD_Spider, self).__init__(*args, **kwargs)
        if query is not None:
            self.start_urls = [
                f'https://www.thegioididong.com/tim-kiem?key={query}'
            ]

    def parse(self, response):
        if response.status == 200:
            tokens = response.css('li.item')
            if len(tokens) <= 0:
                return None

            items = ComputerProductsItem()

            for token in tokens:
                items['retailer'] = 'The gioi di dong'
                items['product_name'] = token.css('a::attr(data-name)').extract()
                items['product_brand'] = token.css('a::attr(data-brand)').extract()
                items['product_price'] = token.css('a::attr(data-price)').extract()
                # if len(items['product_price']) > 1:
                #     separator = ''
                #     price = separator.join(items['product_price'])
                #     items['product_price'] = [price]

                items['product_imglink'] = token.css('a::attr(href)').extract()

                yield items

            # self.page_number += 1
            # next_page = self.start_urls[0] + f'&page={self.page_number}'
            # yield response.follow(next_page, callback=self.parse)

        else:
            print('Undefined response')