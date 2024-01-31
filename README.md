# Web news scaper with Elastic

## Initialize Elasticsearch

Start an elasticsearch instance using docker:

```bash
docker run -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e "http.cors.enabled=true" -e "http.cors.allow-origin=/http?://localhost(:[0-9]+)?/" docker.elastic.co/elasticsearch/elasticsearch:8.1.2
```
```bash
python ElasticSearch.py
```

The indexed data can be visulized at

```bash
$ curl "http://localhost:9200/data"
```

Example of the indexed data
```
{
    "name": "What it will take to save American democracy",
    "link": "https://edition.cnn.com/2022/01/09/opinions/fareed-zakaria-the-fight-to-save-american-democracy-op-ed/index.html",
    "text": "Editor\u2019s Note:On Sunday at 9 p.m. ET, CNN will air Fareed Zakaria\u2019s latest special report, \u201cThe Fight to Save American..."
    "rating": 1
}
```


## Run the program after having initialized Elasticsearch
Start the UI for the engine
```bash
python app.py
```
