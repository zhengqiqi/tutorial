# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
'''
#定义了个字典
class DmozItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    info = scrapy.Field()
    area = scrapy.Field()
    time = scrapy.Field()
    unitPrice = scrapy.Field()

    title1 = scrapy.Field()
    price1 = scrapy.Field()
    info1 = scrapy.Field()
    info2 = scrapy.Field()
    area1 = scrapy.Field()
    unitPrice1 = scrapy.Field()
    name1 = scrapy.Field()