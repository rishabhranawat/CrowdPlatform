from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()

class ElasticsearchOfflineDocuments():
	def generate_search_urls(self, input_title, lesson_outline, source=""):
		s = Search(using=client, index="offline_content")
		q_input_title = Q('match', content=input_title)
		q_lesson_outline = []
		for bullet in lesson_outline:
			q_lesson_outline.append(Q('match', content=bullet))
		q = Q('bool', should=q_lesson_outline, minimum_should_match=1)
		res = s.query(q_input_title).query(q)[:100]
		hits = res.execute()
		links = []
		for hit in hits:
			links.append(hit)
		return links
