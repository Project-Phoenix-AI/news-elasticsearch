# DD2477_Project

## Initialize Elasticsearch

Start an elasticsearch instance using docker:

```bash
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "http.cors.enabled=true" -e "http.cors.allow-origin=/http?://localhost(:[0-9]+)?/" docker.elastic.co/elasticsearch/elasticsearch:8.1.2
```
```bash
python ElasticSearch.py
```