from elasticsearch import Elasticsearch
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.scraper.spiders.newsfeed import Spider
import json


class ElasticSearch():
    def __init__(self, url):
        #'http://localhost:9200'
        self.process = CrawlerProcess()
        self.scraped_items = []
        self.es = Elasticsearch([url])

    def process_item(self, item): # similar to process_item in pipeline
        self.scraped_items.append(item)
        return item

    def crawl(self, **kwargs):
        self.process.crawl(Spider, output_callback=self.process_item, **kwargs)

    def run(self, **kwargs):
        self.process.start()

    # links = soup.find_all('a', class_='article-link')
    def indexLinks(self, query, links):
        self.es.indices.create(index=str(query))
        # Index the articles in Elasticsearch
        for doc in self.scraped_items:
            self.es.index(index=str(query), body=doc)

if __name__ == '__main__':
    es = ElasticSearch('http://localhost:9200')
    es.crawl()
    es.run()
    print("This is the result")
    json_object = json.dumps(es.scraped_items, indent=4)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

    print(len(es.scraped_items))


