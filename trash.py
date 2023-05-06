import json 
from datetime import datetime
from elasticsearch import Elasticsearch
#es = Elasticsearch('http://127.0.0.1:9200')

doc = {
    'author': 'author_name',
    'text': 'Interensting content...',
    'timestamp': datetime.now(),
}

# #resp = es.index(index="test-index", id=1, document=doc)
# #print(resp['result'])

# resp = es.get(index="test-index", id=2)
# print(resp['_source'])

p = "berkan beran"
p= p.split(" ")
print(p)
from collections import defaultdict
query1 = defaultdict(dict)
p = 'cola '
query1['match_phrase']['text'] =p
query1['match_phrase']['slope'] ="2"
print(query1)

