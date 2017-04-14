from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Date, String, \
Nested, Object, Index, MetaField, analyzer, FacetedSearch, \
Q, TermsFacet, DateHistogramFacet, SF, Text, connections

connections.connections.create_connection(hosts=['localhost'])

class OfflineDocument(DocType):
	link = Text()
	source = Text()
	title = Text()
	subject = Text()
	phase = Text()

	content = Text(analyzer='snowball')
	summary = Text(analyzer='snowball')

index = Index(settings.ES_INDEX)
index.settings(number_of_shards=1, number_of_replicas=0)
index.doc_type(OfflineDocument)






