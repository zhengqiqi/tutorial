# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item
'''

import pymysql as pq
'''
def dbHandle():
    conn = pymysql.connect(
        host = "localhost",
        user = "jessica",
        passwd = "@dai77@",
        charset = "utf8",
        use_unicode = False
    )
    return conn
'''

class TmsfPipeline(object):
    def __init__(self):
        self.conn = pq.connect(host='localhost', user='jessica',
                               passwd='@dai77@', db='scrapy', charset='utf8')
        self.cur = self.conn.cursor()

    def process_item(self,item,spider):
        title = item.get("title", "N/A")
        price = item.get("price", "N/A")
        info = item.get("info", "N/A")
        area = item.get("area", "N/A")
        time = item.get("time", "N/A")
        unitPrice = item.get("unitPrice", "N/A")

        sql = "insert into articals(title, price, info, area, time, unitPrice) VALUES (%s, %s, %s, %s, %s, %s)"
        self.cur.execute(sql, (title, price, info, area, time, unitPrice))
        self.conn.commit()
    
    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

'''
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE scrapy")
        sql = "INSERT INTO articals(info,title,price,area,time,unitPrice) VALUES(%s,%s,%s,%s,%s,%s)"
'''