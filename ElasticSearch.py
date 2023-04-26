from elasticsearch import Elasticsearch

"""
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "http.cors.enabled=true" -e "http.cors.allow-origin=/http?://localhost(:[0-9]+)?/" docker.elastic.co/elasticsearch/elasticsearch:8.1.2
"""

class ElasticSearch:
    def __init__(url):
        #'http://localhost:9200'
        self.es = Elasticsearch([url])
        self.idx = 'data'
        self.es.indices.create(index=self.idx)

    def indexLinks(doc):

        # Index the articles in Elasticsearch
        self.es.index(index=self.idx, body={})   


