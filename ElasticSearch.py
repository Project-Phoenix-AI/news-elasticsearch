from elasticsearch import Elasticsearch
import scrapy
from scrapy.crawler import CrawlerProcess
from scraper.scraper.spiders.newsfeed import Spider

"""
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "http.cors.enabled=true" -e "http.cors.allow-origin=/http?://localhost(:[0-9]+)?/" docker.elastic.co/elasticsearch/elasticsearch:8.1.2
"""

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
        for link in links:
            title = link.text
            url = link['href']

            # Extract other metadata as needed
            doc = {
                'title': title,
                'url': url}

            self.es.index(index=str(query), body=doc)

if __name__ == '__main__':
    es = ElasticSearch('http://localhost:9200')
    es.crawl()
    es.run()
    print("This is the result")
    print(es.scraped_items)






