from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator

es = Elasticsearch()

mapping = SearchMappingGenerator()
mapping.add_minimum_should_condition("should", "wildcard", "content", "*heapsort*")
mapping.add_minimum_should_condition("should", "wildcard", "content", "*sorting*")
mapping.edit_minimum_should_number(2)

print(mapping.body)
res = es.search(index="offline_content", body = mapping.body, size=50)
print(res['hits']['total'])
for hit in res['hits']['hits']:
        print(hit['_source']['link'], hit['_score'])
