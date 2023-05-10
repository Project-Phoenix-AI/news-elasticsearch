from collections import defaultdict
import time
from flask import Flask, request, render_template

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
from RetrieveResults import *
import requests
import json
from elasticsearch_dsl import Search

app = Flask(__name__)
#'http://localhost:9200'
es = Elasticsearch('http://localhost:9200')
#s = Search(using =es)


@app.route('/',methods =["GET","POST"])
def index():
    if request.method == 'POST':
        q_ = request.form['query']  # Extract the search query from the form data
        if len(q_.split(' ')) >= 0:
            # Result algorithm
            query = defaultdict(dict)
            query['multi_match']['query'] = q_
            query['multi_match']['fields'] = ['name^2','text']
            query['multi_match']['type'] = 'best_fields'

            # q = Q('bool', should=[
            #     Q('match', content= q_),
            #     Q('match', content={'query': q_, 'operator': 'and'}),
            #     Q('match_phrase', content={'query' : q_,'boost' : 2}),
            #     Q('multi_match', query= q_, fields=['name', 'text^2'])
            # ])

            t_initial = time.time()
            resp = es.search(index="test-index", query=query,size = 50)
            #resp = s.query(q).extra(size=50).collapse(field='name.raw').execute()
            #s = Search(using=es, index='my_index').query(q)
            #s = s.extra(size=1000)  # Increase the result size to 1000 hits
            #s = s.aggs.bucket('name','',)  # Collapse the results by the 'name' field
            #s = s.aggs.bucket('name_terms', 'terms', field='name', size=10000)#.metric('top_hits', 'top_hits', size=1)
            #resp = s.execute()
            t_final = time.time()
            number_of_results = resp['hits']['total']['value']
            results = resp['hits']['hits']
            took = round((t_final - t_initial),2)
            return render_template('/search_results.html',results=results, number_of_results = number_of_results,took = took)
    return render_template('/index.html')




@app.route('/search/<name>', methods=['POST'])
def search(name):
    q_ = request.form['query']  # Extract the search query from the form data
    if len(q_.split(' ')) >= 0:
        # Result algorithm
        query = defaultdict(dict)
        query['multi_match']['query'] = q_
        query['multi_match']['fields'] = ['name^2','text']
        query['multi_match']['type'] = 'best_fields'

        # q = Q('bool', should=[
        #     Q('match', content= q_),
        #     Q('match', content={'query': q_, 'operator': 'and'}),
        #     Q('match_phrase', content={'query' : q_,'boost' : 2}),
        #     Q('multi_match', query= q_, fields=['name', 'text^2'])
        # ])

        t_initial = time.time()
        resp = es.search(index="test-index", query=query,size = 50)
        #resp = s.query(q).extra(size=50).collapse(field='name.raw').execute()
        #s = Search(using=es, index='my_index').query(q)
        #s = s.extra(size=1000)  # Increase the result size to 1000 hits
        #s = s.aggs.bucket('name','',)  # Collapse the results by the 'name' field
        #s = s.aggs.bucket('name_terms', 'terms', field='name', size=10000)#.metric('top_hits', 'top_hits', size=1)
        #resp = s.execute()
        t_final = time.time()
        number_of_results = resp['hits']['total']['value']
        results = resp['hits']['hits']
        took = round((t_final - t_initial),2)
        return render_template('/search_results.html',results=results, number_of_results = number_of_results,took = took)
    return render_template('/index.html')

@app.route('/update', methods=['POST'])
def update():
    #print(request.form)
    result_id = request.form.get('result-id')
    data_ranking = float(request.form.get('data-ranking'))
    increment = float(request.form.get('increment'))

    # Update the data ranking of the document with result id
    data_ranking += increment
    if data_ranking < 0.5:
        data_ranking = 0.5
    elif data_ranking > 2.5:
        data_ranking = 2.5
    print(result_id,data_ranking,increment)
    doc = defaultdict(dict)
    doc['doc']['ranking'] = data_ranking    
    
    es.update(index="test-index", id=int(result_id), body=doc)
    # do something with the result_id and data_ranking data
    return render_template('/index.html')



if __name__ == '__main__':
    app.run(host= 'localhost',port = 8000,debug=True)




