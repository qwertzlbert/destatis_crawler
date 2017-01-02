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

##Limits
With this little tool it's only possible to get an index of the data available on Destatis. Direct download links are not possible, because the downloadlinks rely on a session id which will decay after a short time. However you could use this index with the provided overview links to download some data "on demand" with an additional crawler or some other tool. 
