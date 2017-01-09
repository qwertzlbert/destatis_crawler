# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DestatisAvailable(scrapy.Item):
    title = scrapy.Field()
    ID = scrapy.Field()
    url = scrapy.Field()
    last_updated = scrapy.Field()
    
class DestatisDownloadUrls(scrapy.Item):
    csv = scrapy.Field()
    html = scrapy.Field()
