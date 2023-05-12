import sys
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from computer_products.spiders.phongvu import PhongVu_Spider
from computer_products.spiders.gearvn import GearVN_Spider
from computer_products.spiders.hanoicomputer import HaNoiComputer_Spider

def clear_old_result():
    crawled_results_dir = os.path.join(os.getcwd(), 'crawl_results')
    for filename in os.listdir(crawled_results_dir):
        if filename.endswith('.json'):
            os.remove(os.path.join(crawled_results_dir, filename))

def merge_result(category=None):
    result = []
    crawled_results_dir = os.path.join(os.getcwd(), 'crawl_results')
    for filename in os.listdir(crawled_results_dir):
        if filename.endswith('.json'):
            with open(os.path.join(crawled_results_dir, filename), 'r', encoding='utf-8') as f:
                if os.path.getsize(os.path.join(crawled_results_dir, filename)) > 0:
                    crawl_result = json.load(f)
                    result += crawl_result
    with open(f'merged_results/{category}.json', 'w') as f:
        json.dump(result, f, indent=4)

settings = get_project_settings()
process = CrawlerProcess(settings)
def main(category=None):
    clear_old_result()

    process.crawl(PhongVu_Spider, category=category)
    process.crawl(GearVN_Spider, category=category)
    # process.crawl(HaNoiComputer_Spider, query=query)
    process.start()

    merge_result(category=category)

main(category=sys.argv[1])