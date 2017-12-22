from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator

es = Elasticsearch()

mapping = SearchMappingGenerator()
mapping.add_minimum_should_condition("should", "wildcard", "content", "*heapsort*")
mapping.add_minimum_should_condition("should", "wildcard", "content", "*sorting*")
mapping.edit_minimum_should_number(2)

print(mapping.body)
res = es.search(index="offline_content", body = {'query':{'match':{'link':'https://www.knewton.com/wp-content/uploads/knewton-adaptive-learning-whitepaper.pdf'}}})
print(res['hits']['total'])
for hit in res['hits']['hits']:
        print(hit['_source']['pk'], hit['_source']['link'], hit['_score'])
