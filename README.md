# destatis_crawler
Just a simple crawler to get a full index of destatis (Federal Statistical Office of Germany) statistics to use for further processing 

This is just a basic crawler to get a full list of all statistics of the Destatis Genesis database. 
The output you can use for further processing. 


##Requirements
To get this work you just need to install the scrapy framework via pip (pip install scrapy), your favorite package manager or directly via the [Scrapy GitHub reposetory](https://github.com/scrapy/scrapy)


##How to
To run the crawler you just need to enter the command: 

```scrapy crawl destatis```

To get a csv output enter the command: 

  ```scrapy crawl destatis -o output.csv```
  
For json output: 

  ```scrapy crawl destatis -o output.json```
