# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy_handler import scrapy_handler

class DestatisScrapyPipeline(object):
    '''This pipeline processes the items received from the spiders to 
    make them available for the scrapy_handler class to feed the output
    to other applications'''
        
    # this function just sends a dict of the items to the scrapy_handler class
    def process_item(self, item, spider):
        scrapy_handler.return_dict(dict(item))
        return item
