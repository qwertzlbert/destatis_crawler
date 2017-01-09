# destatis_crawler
Just a simple crawler to get a full index of destatis (Federal Statistical Office of Germany) statistics to use for further processing 

This is just a basic crawler to get a full list of all statistics of the Destatis Genesis database. 
You can use the output for further processing. 


##Requirements
To get this work you just need to install the scrapy framework via pip (`pip install scrapy`), your favorite package manager or directly via the [Scrapy GitHub repository](https://github.com/scrapy/scrapy)


##How to
To run the crawler you just need to enter the command: 

```scrapy crawl destatis```

To get a csv output enter the command: 

  ```scrapy crawl destatis -o output.csv```
  
For json output: 

  ```scrapy crawl destatis -o output.json```

##Handler
With the scrapy_handler class inside scrapy_handler.py you can call the scrapy spider and receive a dict of the links (either the full list of all stats or the direct download link) which you can use for further processing, without the need to read the output from another file.

call `get_list()` to receive a list of all stats and `download_csv(url)` with the URL of a statistic overview page as argument to receive the direct download link.
