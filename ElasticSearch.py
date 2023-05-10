import time
from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.scraper.spiders.newsfeed import Spider
import json
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q
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
    # es = ElasticSearch('http://localhost:9200')
    # es.crawl()
    # es.run()
    # print("This is the result")
    # es.get_scraped_items()

    # # # json_object = json.dumps(es.scraped_items, indent=4)
    # # # with open("sample.json", "w") as outfile:
    # # #     outfile.write(json_object)

    # es.index_docs('test-index')
    es = Elasticsearch('http://localhost:9200')

    s = Search(using =es)
    s = s.using(es)

    #resp = es.get(index="test-index", id=2)
    #print(resp['_source'])
    #print(len(es.scraped_items))

    # query1 = defaultdict(dict)
    # query1['match_phrase']['text'] ="pizza"
    # #query1['match_phrase']['slope'] ="2"
    # print(query1)

    # #q['match_phrase']['text'] = "cluster"
    # #q = q.format(query_ = "pizza")
    # #print(' = query = ')
    # #print(q)
    # resp = es.es.search(index="test_index", query = query1)#{"match_all":{"text":"pizza"}})
    # resp = resp['hits']
    q_ = 'pizza'
    
    
    print(q_)
    # print(resp)
    query = defaultdict(dict)
    query['multi_match']['query'] = 'world'
    query['multi_match']['fields'] = ['name','text']
    query['multi_match']['type'] = 'phrase'


    print(q_)
    # print(resp)
 

   
    

    t_initial = time.time()
    #resp = es.search(index="test-index", query=query)
    resp = s.query(q1).execute()
    t_final = time.time()
    print("time taken", t_final - t_initial)

    print('HITS',resp.keys())
    print(resp['hits'])
    print(resp['hits']['hits'])



    # print('total',resp['hits']['total'])
    # print('max_score',resp['hits']['max_score'])
    # print('hits',resp['hits']['hits'][0])


    # #resp = resp['hits']['hits']['_source']
    # results = resp
    # print(results)




