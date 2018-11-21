# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XuanshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    novelname = scrapy.Field()
    author = scrapy.Field()
    novelid = scrapy.Field()
    noveltype = scrapy.Field()
    novelsize = scrapy.Field()
    downloadNum = scrapy.Field()
    novelurl = scrapy.Field()
    txtdownload=scrapy.Field()
    zipdownload=scrapy.Field()
