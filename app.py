from flask import Flask, request, render_template
#from elasticsearch import Elasticsearch
from ElasticSearch import ElasticSearch

app = Flask(__name__, template_folder='.')

es = ElasticSearch('http://localhost:9200')

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']  # Extract the search query from the form data

    if query >= 0:
        # Result algorithm
        pass
    else:
        res = es.index(index=es.idx, body={'query': {'match': {'content': query}}})

    return render_template('search_results.html', res)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    article_id = request.form.get('article_id')
    feedback = request.form.get('feedback')
    # Do something with the feedback (e.g., store it in a database)
    return app.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
