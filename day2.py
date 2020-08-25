from datetime import datetime
from elasticsearch import Elasticsearch

es_host = 'localhost:9200'
index_name = 'fwiratam'

es = Elasticsearch([es_host])

doc = {
    'author': 'fwiratam',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.utcnow(),
}
// HTTP POST
res = es.index(index=index_name, id=1, body=doc)
print(res['result'])

// HTTP GET
res = es.get(index=index_name, id=1)
print(res['_source'])

es.indices.refresh(index=index_name)

// HTTP POST
res = es.search(index=index_name, body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

