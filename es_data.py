from elasticsearch import Elasticsearch
es = Elasticsearch()



body = {"query": {"wildcard":{
    "link": "*edu"
}}}

res = es.search(index="offline_content", body = body)
print(res['hits']['total'])


#for hit in res['hits']['hits']
#    if("wikipedia" not in hit['_source']['link']):
#        print(hit['_source']['link'])
