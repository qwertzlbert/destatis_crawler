import scrapy
from scrapy.utils.response import open_in_browser
import urllib
from collections import OrderedDict
from ..items import DestatisAvailable, DestatisDownloadUrls
import datetime

# start scrapy with 'scrapy crawl destatis'
# To get an output use something like 'scrapy crawl destatis -o output.csv' 
# for csv output or 'scrapy crawl destatis -o output.json' for json output
 


class DestatisSpider(scrapy.Spider):
    '''spider to crawl the complete table list to get all table links and information to this tables.
    for some reason the links for the statistics returned from this spider are not session based and
    they are permanent. So you can use them as quicklinks to get to the statistics'''
    
    name = "destatis"
    
    # start at genesis base url, because session ids are used. 
    start_urls = [
        'https://www-genesis.destatis.de/genesis/online',
    ]    
    
    def parse(self, response):
        
        # search for link to tables 
        table_link = response.css("a#id303::attr(href)").extract_first()
        
        if table_link is not None:
            
            table_link = response.urljoin(table_link)
            
            # follow link to table page
            yield scrapy.Request(table_link, callback=self.parse_table, meta={'x_value': 0})
        

    def parse_table(self, response):
        ''' parse content on table page '''
        
        tables = response.css('table.verzeichnis tr')
        # remove table header
        tables.pop(0)
        
        for entry in tables:
            availstats = DestatisAvailable()
            availstats['title'] = entry.css('a::text')[1].extract(),             
            availstats['url'] = entry.css('a::attr(href)')[1].extract(),             
            availstats['ID'] = entry.css('a::text')[0].extract(),   
            availstats['last_updated'] = datetime.datetime.now(), 
            yield availstats

        # extract action address out of next page top form
        next_page = response.css('form::attr(action)')[3].extract()
        if next_page is not None:
            # get x value from response
            x_value = response.meta['x_value']
            x_value = x_value + 1
            next_page = response.urljoin(next_page)
            
            # follow link to next page. Make request as POST to get to next page. 
            # Request needs forward.x and forward.y as POST data. 
            # I'm not sure how this values are calculated or where they come from, 
            # but it seems like you can use any value for a successfull request. 
            # You only need to make sure, that you don't use a number twice.
            # For this I just used a simple counter to get different values .
            yield scrapy.FormRequest(url=next_page, formdata={'forward.x': str(x_value), 'forward.y': '0'}, callback=self.parse_table, meta={'x_value': x_value})


class DestatisDownload(scrapy.Spider):
    '''spider to get the session based download link for html and csv files, so be quick in processing the links.
    provide the url of the table as a tag like this: "scrapy crawl -a url="heregoestheURL" " '''
    
    name = "destatis-download"
    
    # starts the request 
    def start_requests(self):
        # get the url out of the tag
        url = getattr(self, 'url', None)
        yield scrapy.Request(url, self.parse_download_page)
   
    # parses the statistics overview page to get to the downloadpage
    def parse_download_page(self, response):
       
        # create a querystring to get to the downloadpage
        ## this entries should be enough to get all content in the download file
        querystring = OrderedDict([
                        ('operation','abruftabelleBearbeiten'),
                        ('levelindex', '1'),
                        ('levelid', response.css('input[name=levelid]::attr(value)').extract_first()),
                        ('auswahloperation','abruftabelleAuspraegungAuswaehlen'),
                        ('auswahlverzeichnis','ordnungsstruktur'),
                        ('auswahlziel','werteabruf'),
                        ('selectionname', response.css('input[name=selectionname]::attr(value)').extract_first()),
                        ('auswahltext',''),
                        ('werteabruf','Value retrieval')
                        ])

        querystring = urllib.parse.urlencode(querystring)
        url = response.css('form::attr(action)')[1].extract()
        
        ## this part is a bit weird. For some reason you have to change the
        ## numbers of this part of the url "tomcat_GO_2_2" otherwise you 
        ## can't proceed to the download page. 
        ## Somehow it's enough to change the first number to eather 1 or 2
        ## depending on which number is already present. The second number
        ## is always (at least as I can say) between 1 and 3.
        
        # make the url usable 
        base_url = url.rsplit('_',2)[0]
        first_parameter = url.rsplit('_',2)[1]
        second_parameter = url.rsplit('_',2)[2]
        if first_parameter == '1':
            first_parameter = '2'
        else:
            first_parameter = '1'
        
        url = base_url + '_' + first_parameter + '_' + second_parameter

        url = url + '?' + querystring

        request = scrapy.Request(url=url ,callback = self.parse_download_link)
                
        yield request
        
    # get the download links from the download page
    def parse_download_link(self, response):
        urls = DestatisDownloadUrls()
        urls['csv'] = response.css('form::attr(action)')[4].extract()
        urls['html'] = response.css('form::attr(action)')[5].extract() 
        yield urls 
