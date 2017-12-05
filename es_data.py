from elasticsearch import Elasticsearch
es = Elasticsearch()
body = {
	"query": {
            "bool":{
                "must_not":{
                    "match":{
                        "link":"wikipedia"
                    }     
                },
                "minimum_should_match" : 1,
                "boost" : 1.0
            },
            "wildcard":{
                "content": "*logistic?regression*"            
            }
	}
}

res = es.search(index="offline_content", body = body, size=500)
print(res['hits']['total'])
for hit in res['hits']['hits']:
        print(hit['_source']['link'])
