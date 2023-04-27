import scrapy
import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from computer_products.spiders.phongvu import PhongVu_Spider
from computer_products.spiders.gearvn import GearVN_Spider
from computer_products.spiders.hanoicomputer import HaNoiComputer_Spider

settings = get_project_settings()
process = CrawlerProcess(settings)

def main(query=''):
    process.crawl(PhongVu_Spider, query=query)
    process.crawl(GearVN_Spider, query=query)
    process.crawl(HaNoiComputer_Spider, query=query)
    process.start() # the script will block here until all crawling jobs are finished

main(sys.argv[1])