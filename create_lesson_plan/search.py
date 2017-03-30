from django.conf import settings

from elasticsearch import connections
from elasticsearch_dsl import DocType, Date, String, \
Nested, Object, Index, MetaField, analyzer, FacetedSearch, \
Q, TermsFacet, DateHistogramFacet, SF, Text

connections.create_connection(hosts=['localhost'])

html_strip = analyzer('html_strip',
    tokenizer="standard", 
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

class OfflineDocument(DocType):
    date_scraped = Date()
    content = Text(analyzer='snowball')
    link = Text()
    source = Text()


index = Index(settings.ES_CLIENT)
index.settings(number_of_shards=1, number_of_replicas=0)
index.doc_type(OfflineDocument)






