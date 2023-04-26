from flask import Flask, request, render_template
#from elasticsearch import Elasticsearch
from ElasticSearch import ElasticSearch
from RetrieveResults import *

app = Flask(__name__, template_folder='.')
es = ElasticSearch('http://localhost:9200')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']  # Extract the search query from the form data

    if len(query) >= 0:
        # Result algorithm
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
        return render_template('search_results.html', results)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    article_id = request.form.get('article_id')
    feedback = request.form.get('feedback')
    # Do something with the feedback (e.g., store it in a database)
    return app.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
