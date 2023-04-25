# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import mysql.connector

class ComputerProductsPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        db_info = {}
        with open('computer_products/database.txt', 'r') as f:
            info = f.readlines()
            db_info['host'] = info[0].strip()
            db_info['user'] = info[1].strip()
            db_info['passwd'] = info[2].strip()
            db_info['database'] = info[3].strip()

        self.conn = mysql.connector.connect(host=db_info['host'], user=db_info['user'], passwd=db_info['passwd'], database=db_info['database'])
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""drop table if exists PRODUCTS""")
        self.curr.execute(
            """
            create table PRODUCTS (
                retailer text,
                product_name text,
                product_brand text,
                product_price text,
                product_imglink text
            )
            """
        )

    def process_item(self, item, spider):
        self.store_item(item)
        return item

    def store_item(self, item):
        self.curr.execute("""insert into PRODUCTS values (%s, %s, %s, %s, %s)""",
                          (item['retailer'],
                           item['product_name'][0],
                           item['product_brand'][0],
                           item['product_price'][0],
                           item['product_imglink'][0],
                          ))
        self.conn.commit()

