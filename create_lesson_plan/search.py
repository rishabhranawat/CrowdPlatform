from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Date, String, \
Nested, Object, Index, MetaField, analyzer, FacetedSearch, \
Q, TermsFacet, DateHistogramFacet, SF, Text, connections, Attachment, A, Integer

connections.connections.create_connection(hosts=['localhost'])

class OfflineDocument(DocType):
	link = Text()
	source = Text()
	title = Text()
	subject = Text()
	phase = Text()
	pk = Integer()
	content = Text(analyzer='snowball')
	summary = Text(analyzer='snowball')

index = Index(settings.ES_INDEX)
index.settings(number_of_shards=1, number_of_replicas=0)
index.doc_type(OfflineDocument)



# es.indices.delete('offline_content')
# with open("16au_hw1.pdf") as f:
# 	d = f.read()
# data = base64.b64encode(d)
# body = {
# 	'link' : 'go.com',
# 	'source': 'my source', 
# 	'subject' : 'computer science',
# 	'phase': 'A',
# 	'pk': 10,
# 	'content': 'content',
# 	'summary': 'summary',
# 	'data': data
# }
# body = json.dumps(body)
# es.index(index='offline_content', doc_type="offline_document", pipeline="attachment",body=body)



# databody = json.dumps({'data': data})
# es.index(index='offline_content', doc_type='offline_document', pipeline="attachment",body=databody, id="AVuThQM2PwuoeJj9Z7P_")