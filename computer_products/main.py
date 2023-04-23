import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from computer_products.spiders.phongvu import PhongVu_Spider
from computer_products.spiders.gearvn import GearVN_Spider

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(PhongVu_Spider, query='ASUS')
process.crawl(GearVN_Spider, query='ASUS')
process.start() # the script will block here until all crawling jobs are finished