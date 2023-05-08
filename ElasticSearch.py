from elasticsearch import Elasticsearch
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.scraper.spiders.newsfeed import Spider
import json

from collections import defaultdict
class ElasticSearch():
    def __init__(self, url):
        #'http://localhost:9200'
        self.id_ = 0
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

    def index_docs(self,index):
        for i,item in enumerate(self.scraped_items):
            doc = json.dumps(item, indent=4)
            resp = self.es.index(index= index, id=self.id_, document=doc)
            self.id_ += 1 



    def get_scraped_items(self):
        '''
        helper function to understand the scraped items
        '''
        for i,item in enumerate(self.scraped_items):
            print(item)
            print('=======================')
            if i == 3:
                break
        




if __name__ == '__main__':
    es = ElasticSearch('http://localhost:9200')
    es.crawl()
    es.run()
    print("This is the result")
    es.get_scraped_items()

    #json_object = json.dumps(es.scraped_items, indent=4)
    #with open("sample.json", "w") as outfile:
    #   outfile.write(json_object)

    es.index_docs('test_index')


    #resp = es.get(index="test-index", id=2)
    #print(resp['_source'])
    #print(len(es.scraped_items))

    # q = {"match_phrase":{
    #             "text" : "pizza",
    #                     } ,
                        
    # }

    # query1 = defaultdict(dict)
    # query1['match_phrase']['text'] ="pizza"
    # #query1['match_phrase']['slope'] ="2"
    # print(query1)


    
    # #q['match_phrase']['text'] = "cluster"
    # #q = q.format(query_ = "pizza")
    # #print(' = query = ')
    # #print(q)
    resp = es.es.search(index="test_index", query = query1)#{"match_all":{"text":"pizza"}})
    # resp = resp['hits']

    # print(resp)
    



