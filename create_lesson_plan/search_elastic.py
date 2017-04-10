from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()

class ElasticsearchOfflineDocuments():
	def generate_search_urls(self, input_title, lesson_outline, limit):
		s = Search(using=client, index="nicaragua_wiki_3")
		q_input_title = Q('match', content=input_title)
		q_lesson_outline = []
		for bullet in lesson_outline:
			q_lesson_outline.append(Q('match', content=bullet))
		q = Q('bool', should=q_lesson_outline, minimum_should_match=1)
		res = s.query(q_input_title)
		hits = res.execute()
		
		all_links = []
		for i in range(0, limit, 1):
			hit = hits[i]
			if(hit.meta.score > 0):
				print(hit.meta.score, hit.link)
				link_details = {
					'title': '',
					'Url' : hit.link,
					'Description' : ''
				}
				all_links.append(link_details)
		return all_links

