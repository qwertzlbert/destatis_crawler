import scrapy

# start scrapy with 'scrapy crawl destatis'
# To get an output use something like 'scrapy crawl destatis -o output.csv' 
# for csv output or 'scrapy crawl destatis -o output.json' for json output

class DestatisSpider(scrapy.Spider):
    
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
            
            yield{
                'title': entry.css('a::text')[1].extract(),
                'href':entry.css('a::attr(href)')[1].extract(),
                'id':entry.css('a::text')[0].extract(),
            }
        
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
