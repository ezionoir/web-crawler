import scrapy
from ..items import ComputerProductsItem

class PhongVu_Spider(scrapy.Spider):
    name = 'PhongVu'
    page_number = 1
    start_urls = [
        'https://phongvu.vn/'
    ]

    def __init__(self, query=None, *args, **kwargs):
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
                items['retailer'] = 'Phong Vu'
                items['product_name'] = token.css('div.css-1ybkowq div h3::text').extract()
                items['product_brand'] = token.css('div.css-68cx5s div::text').extract()
                # items['product_price'] = token.css('div.css-kgkvir div div.att-product-detail-latest-price::text').extract()
                items['product_price'] = token.css('div.css-kgkvir > div.css-1co26wt > div::text').extract()
                if len(items['product_price']) > 1:
                    separator = ''
                    price = separator.join(items['product_price'])
                    items['product_price'] = [price]

                items['product_imglink'] = token.css('div.css-1v97aik div div img::attr(src)').extract()

                yield items

            self.page_number += 1
            next_page = self.start_urls[0] + f'&page={self.page_number}'
            yield response.follow(next_page, callback=self.parse)