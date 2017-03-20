from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text,String, Date, Integer

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from .models import lesson

connections.create_connection()

class lessonIndex(DocType):
	user_name = Text()
	subject = Text()
 	course_name = Text()
	# lesson_title = Text()
	grade = Text()
	bullets = Text()
	stage = Integer()


def bulk_indexing():
	lessonIndex.init(index='lesson')
	es = Elasticsearch()
	bulk(client=es, actions=(b.indexing for b in lesson.objects.all().iterator()))


 
