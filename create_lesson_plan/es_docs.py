from datetime import datetime
from elasticsearch_dsl import DocType, Date, Nested, Boolean, \
analyzer, InnerObjectWrapper, Completion, Keyword, Text

class esOfflineDoc(DocType):
	link = Text()
	content = Text(analyzer='snowball')
	scraped_date = Date()
	
	class Meta:
		index = 'OfflineDocument'
	
	def save(self, **kwargs):
		return super().save(**kwargs)


	
