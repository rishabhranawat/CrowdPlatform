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
                    q_lesson_outline.append(Q("match", content=bullet))
		q_outlines = Q('bool', should=q_lesson_outline, minimum_should_match=0)
		return q_outlines		

	def get_query_link(self):
		q_syllabus = ~Q("wildcard", link="*syllabus*")
                q_wiki = ~Q("wildcard", link="*wikipedia*")
                q_edu = Q("wildcard", link="*\.pdf*")
                q_link = q_syllabus & q_wiki & q_edu
	        
                return q_link
	
	def get_required_links(self, hits):
		links = []
		for hit in hits:
			if("syllabus" not in str(hit.link)): links.append(hit.link)
		return set(links)

	def generate_search_urls(self, input_title, lesson_outline, source=""):
		s = Search(using=client, index="offline_content")

                print(lesson_outline)
		#input_title_q = self.get_query_input_title(input_title)
		#link_q = self.get_query_link()
                lesson_outline_q = self.get_query_lesson_outline(lesson_outline)

                results = set()
                q_wiki = Q("wildcard", link="*wikipedia*")
                q_edu = Q("wildcard", link="*\.edu*")
                q_must = Q("wildcard", content="*"+lesson_outline[0].replace(" ", "\ ")+"*")
                q_edu_pdf = Q("wildcard", link="*.pdf*")
                q_random = ~q_wiki & ~q_edu

                query_types= [(q_wiki, 2), (q_edu, 3),(q_edu_pdf, 10), (q_random, 2)]
                for each_type in query_types:
                    query = lesson_outline_q & each_type[0]
                    #res = s.query(query)[:each_type[1]]
                    res = s.query(query)[:each_type[1]]
                    hits = res.execute()
                    results |= self.get_required_links(hits)

                return results

	def get_graph_based_queries(self, query):
		queries = self.gqf.get_queries(query)
                if(len(queries) == 0): return [query]
                else: return queries
