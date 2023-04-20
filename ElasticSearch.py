from elasticsearch import Elasticsearch

class ElasticSearch:
    def __init__():
        self.es = Elasticsearch(['http://localhost:9200'])

    # links = soup.find_all('a', class_='article-link')
    def indexLinks(query, links):
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


