from django.conf import settings

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from elasticsearch_dsl import DocType, Date, String, \
Nested, Object, Index, MetaField, analyzer, FacetedSearch, \
Q, TermsFacet, DateHistogramFacet, SF, Text, connections, Attachment, A, Integer


connections.connections.create_connection(hosts=['localhost'])

class OfflineDocumentIndex(DocType):
	link = Text()
	source = Text()
	title = Text()
	subject = Text()
	phase = Text()
	pk = Integer()
	content = Text(analyzer='snowball')
	summary = Text(analyzer='snowball')

	class Meta:
		index = "offline_content_final"
		pipeline = "attachment"


# index = Index(settings.ES_INDEX)
# index.settings(number_of_shards=1, number_of_replicas=0)
# index.doc_type(OfflineDocument)

def bulk_indexing():
	from create_lesson_plan.models import OfflineDocument
	OfflineDocumentIndex.init(index=settings.ES_INDEX)
	es = Elasticsearch()
	bulk(client=es,actions=(b.indexing() 
		for b in OfflineDocument.objects.all().iterator()))
