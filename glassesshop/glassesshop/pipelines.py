# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import logging


class SQLitePipeline(object):

    def open_spider(self, spider):

        self.connection = sqlite3.connect(database="shop.db")
        self.c = self.connection.cursor()

        try:
            self.c.execute("""
                CREATE TABLE glasses (
                    name TEXT,
                    url TEXT,
                    price TEXT,
                    img_url TEXT
                )
            """)
        except sqlite3.OperationalError as err:
            logging.warning(msg=err)
        else:
            self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):

        try:
            self.c.execute("""
                INSERT INTO glasses (name, url, price, img_url) VALUES (
                    ?, ?, ?, ?
                )
            """, (
                item["name"], item["url"], item["price"], item["img_url"]
            ))
        except sqlite3.IntegrityError:
            pass
        else:
            self.connection.commit()
