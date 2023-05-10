import sys
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from computer_products.spiders.phongvu import PhongVu_Spider
from computer_products.spiders.gearvn import GearVN_Spider
from computer_products.spiders.hanoicomputer import HaNoiComputer_Spider

def clear_old_result():
    current_path = os.getcwd()
    for filename in os.listdir(current_path):
        if filename.endswith('.json'):
            os.remove(os.path.join(current_path, filename))

def merge_result():
    result = []
    current_path = os.getcwd()
    for filename in os.listdir(current_path):
        if filename.endswith('.json'):
            with open(filename, 'r', encoding='utf-8') as f:
                crawl_result = json.load(f)
                result += crawl_result
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)

settings = get_project_settings()
process = CrawlerProcess(settings)
def main(query=None, category=None):
    clear_old_result()

    process.crawl(PhongVu_Spider, query=query)
    process.crawl(GearVN_Spider, query=query)
    process.crawl(HaNoiComputer_Spider, query=query)
    process.start()

    merge_result()

main(query=sys.argv[1])