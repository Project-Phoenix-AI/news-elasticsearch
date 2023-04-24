from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__, template_folder='.')

es = Elasticsearch(['http://localhost:9200'])
index_name = 'my_index'

@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']  # Extract the search query from the form data
    res = es.index(index=index_name, body={'query': {'match': {'content': query}}})
    hits = res['hits']['hits']
    return render_template('search_results.html', hits=hits)

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    article_id = request.form.get('article_id')
    feedback = request.form.get('feedback')
    # Do something with the feedback (e.g., store it in a database)
    return app.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
