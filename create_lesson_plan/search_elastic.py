from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from graph_query.query_formulator_poc import GraphQueryFormulator


client = Elasticsearch()

class ElasticsearchOfflineDocuments():
	def __init__(self):
		self.gqf = GraphQueryFormulator()	

	def get_query_input_title(self, input_title):
		q_input_title = Q("match", content=input_title)
		return q_input_title

	def get_query_lesson_outline(self, lesson_outline):
		q_lesson_outline = []
		for bullet in lesson_outline:
			q_lesson_outline.append(Q('match', content=bullet))
		q_outlines = Q('bool', should=q_lesson_outline, minimum_should_match=1)
		return q_outlines		

	def get_query_link(self):
		q_syllabus = ~Q("match", link="syllabus")
                q_edu = Q("wildcard", link="*edu*")
                q_link = q_syllabus & q_edu
		return q_link
	
	def get_required_links(self, hits):
		links = []
		for hit in hits:
			if("syllabus" not in str(hit.link)): links.append(hit.link)
		return links

	def generate_search_urls(self, input_title, lesson_outline, source=""):
		s = Search(using=client, index="offline_content")
		
		input_title_q = self.get_query_input_title(input_title)
		link_q = self.get_query_link()

		lesson_outline = self.get_graph_based_queries(lesson_outline[0])
		lesson_outline_q = self.get_query_lesson_outline(lesson_outline)

		query = lesson_outline_q &input_title_q & link_q
		res = s.query(query)[:100]
		hits = res.execute()
			
		return self.get_required_links(hits)

	def get_graph_based_queries(self, query):
		queries = self.gqf.get_queries(query)
                if(len(queries) == 0): return [query]
                else: return queries
