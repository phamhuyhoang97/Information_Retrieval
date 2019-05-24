# Information_Retrieval
Project for subject Information Retrieval: Build a tool for crawling data from the internet, then build a search engine. 
* The Project uses:
  - Scrapy + Splash: Crawl data from websites (kenh14.vn and dantri.com)
  - MySQL: Storage data after crawled
  - Elasticsearch + Logstash: Build search engine
* Create Table in database:
  - id: bigint
  - url: varchar(255)
  - title: tinytext
  - time: datetime
  - short_content: mediumtext
  - full_content: longtext
* Crawl data (folder 'news'): 
  - Install enviroment: 
    + Install docker splash: sudo docker pull scrapinghub/splash
    + Run docker splash: sudo docker run -p 8050:8050 scrapinghub/splash
    + Install library scrapy and splash: pip3 install scrapy scrapy-splash
  - Crawl from dantri.com and kenh14.vn
  - Duplicate content Identifier by Jaccard Similarity with data storage in MySQL
  - Config information of your database in file: 
        /news/news/spiders/kenh14_spider.py 
        /news/news/spiders/dantri_spider.py
  - Start crawling:
    + cd news
    + scrapy crawl kenh14
    + scrapy crawl dantri
  (- /news/csvTomysql.py: process data in file your.csv to storage to mysql)
  - Data will storage in mysql database
  - Do crawl with 
* Install Elasticsearch:
  - Install Elasticsearch
  - Install Logstash
  - Create index in ES (elasticsearch.txt)
  - Copy file logstash_mysql.conf to /usr/share/logstash/
  - Push data fro Mysql to index of ES:
      sudo bin/logstash --path.settings /etc/logstash/ -f logstash_mysql.conf
  - Test search in ES:
      cd /src
      python serachEngine.py -i "index" -s "search_word"
* UI in /interface/index.php


