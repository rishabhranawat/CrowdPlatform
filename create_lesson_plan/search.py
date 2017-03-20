from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text,String, Date, Integer

from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from .models import lesson

connections.create_connection()

class lessonIndex(DocType):
	user_name = String()
	subject = String()
 	course_name = String()
	lesson_title = String()
	grade = String()
	bullets = String()
	stage = Integer()

	class Meta:
		index = 'lesson'

def bulk_indexing():
	lessonIndex.init()
	es = Elasticsearch()
	bulk(client=es, actions=(b.indexing for b in lesson.objects.all().iterator()))


 
