from collections import defaultdict
from flask import Flask, request, render_template
#from ElasticSearch import ElasticSearch
from elasticsearch import Elasticsearch

from RetrieveResults import *
import requests
import json
app = Flask(__name__)
#'http://localhost:9200'
es = Elasticsearch('http://localhost:9200')


@app.route('/',methods =["GET","POST"])
def index():
    if request.method == 'POST':
        q = request.form['query']  # Extract the search query from the form data
        results = -1
        if len(q.split(' ')) >= 0:
            # Result algorithm
            query = defaultdict(dict)
            #query['match']['text'] = q

            query['query_string']['fields'] = ["title","text"]
            query['query_string']['query'] = q
            query['query_string']['default_operator'] = 'OR'



            resp = es.search(index="test_index", query=query)
            results = resp['hits']['hits']

            # print(type(results))
            # print(results)
            return render_template('/search_results.html',results=results)
    return render_template('/index.html')









@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']  # Extract the search query from the form data
    results = -1
    if len(query.split(' ')) >= 0:
        # Result algorithm
        query = defaultdict(dict)
        query['match']['text'] = query
        resp = es.search(index="test-index", query=query)
        resp = resp['_source']
        results = resp
        '''
        
        terms = [term.term for term in query.queryterm]
        results = []
        all_matches={}

        # for each query term, retrieve its postings list and add up scores for each document
        for term in terms:
            for key, value in es.items():
                if isinstance(value, dict):
                    for inner_key, inner_value in value.items():
                        if term in (inner_value['text'] or inner_value['title']):
                            if key not in all_matches:
                                all_matches[key]= value

            results = RankedRetrieval(all_matches, term, es)
        #  Sort the dictionary by decreasing score
        results = {k: v for k, v in sorted(results.items(), key=lambda x: x[1]['score'], reverse=True)}
        return render_template('search_results.html', results)
    else:

        results = es.get(index='data')
        '''
    

        return render_template('/search_results.html', results)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    article_id = request.form.get('article_id')
    feedback = request.form.get('feedback')
    # Do something with the feedback (e.g., store it in a database)
    return app.redirect('/')


if __name__ == '__main__':
    app.run(host= 'localhost',port = 8000,debug=True)