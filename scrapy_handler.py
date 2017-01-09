import scrapy 
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class scrapy_handler:
    '''class to handle the scrapy spiders and make the outputs available for
    further processing.'''
    
    items = []
    
    def get_list():
        '''calls the destatis spider to collect all statistics'''
    
        process = CrawlerProcess(get_project_settings())
        process.crawl('destatis')
        # start the crawling
        process.start()
        # return the collected items as a list of dicts
        return scrapy_handler.items
    
    def download_csv(url):
        '''calls the destatis downloadlink crawler to get the direct download
        links'''
    
        process = CrawlerProcess(get_project_settings())
        process.crawl('destatis-download', url=url)
        # start the crawling
        process.start()
        # return the collected items as alist of dicts
        return scrapy_handler.items
 
    def return_dict(item):
        '''function to collect the items and add them to the items list'''
        scrapy_handler.items.append(item)
    
