from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from graph_query.query_formulator_poc import GraphQueryFormulator


client = Elasticsearch()

class ElasticsearchOfflineDocuments():
	def __init__(self):
		self.gqf = GraphQueryFormulator()	


	'''
	Must contain at least 1 bullet point as a wildcard
	in the content.
	'''
	def get_query_lesson_outline(self, lesson_outline):
		q_lesson_outline = []
		for bullet in lesson_outline:
                    q_lesson_outline.append(Q("match", content=bullet))
		q_outlines = Q('bool', should=q_lesson_outline, minimum_should_match=0)
                return q_outlines


	def get_query_types(self,lesson_outline,  phase):
		if(phase == 1):
			lesson_outline_q = self.get_query_lesson_outline(lesson_outline)
			q_wiki = Q("wildcard", link="*wikipedia*")
			q_edu = Q("wildcard", link="*\.edu")
			q_edu_pdf = Q("wildcard", link="*\.pdf") & q_edu
			q_random = ~q_edu & ~q_wiki & ~q_edu_pdf
			return [(q_wiki, 2), (q_edu, 3), (q_edu_pdf, 3), (q_random, 3)]
		else:
			lesson_outline_q = self.get_query_lesson_outline(lesson_outline)
			q_link_final = Q("wildcard", link="*final*")
			q_link_midterm = Q("wildcard", link="*midterm*")
			q_link_solution = Q("wildcard", link="*exam*")
			q_link_homework = Q("wildcard", link="*solution*")

			q_link = (q_link_homework or q_link_midterm 
			or q_link_solution or q_link_final)

			q_edu = Q("wildcard", link="*\.edu")
			q_edu_pdf = Q("wildcard", link="*\.pdf") & q_edu

			return [(q_link, 10)]
	
	'''
	Cleaning
	'''
	def get_required_links(self, hits):
		links = []
		for hit in hits:
                        print(hit.meta)
			if("syllabus" not in str(hit.link)): links.append(hit.link)
		return set(links)

	def generate_search_urls(self, input_title, lesson_outline, phase=1, source=""):
		s = Search(using=client, index="offline_content")
		results = set()
		query_types= self.get_query_types(lesson_outline, phase)
                lesson_outline_q = self.get_query_lesson_outline(lesson_outline) 
                print(lesson_outline[0])
		q_wiki = Q("wildcard", link="*wikipedia*")
                q_edu = Q("wildcard", link="*\.edu*")
                q_must = Q("wildcard", content="*"+lesson_outline[0].replace(" ", "\ ")+"*")
                q_edu_pdf = Q("wildcard", link="*.pdf*")
                q_random = ~q_wiki & ~q_edu
                query_types= [(q_wiki, 4), (q_edu, 5), (q_random, 5)]
                for each_type in query_types:
			query = lesson_outline_q and each_type[0]
                        res = s.query(query)[:each_type[1]]
			hits = res.execute()
                        print(self.get_required_links(hits))
			results |= self.get_required_links(hits)
		return results

# def get_graph_based_queries(self, query):
# 	queries = self.gqf.get_queries(query)
#                if(len(queries) == 0): return [query]

#                else: return queries
# q_wiki = Q("wildcard", link="*wikipedia*")
# q_edu = Q("wildcard", link="*\.edu*")
# q_must = Q("wildcard", content="*"+lesson_outline[0].replace(" ", "\ ")+"*")
# q_edu_pdf = Q("wildcard", link="*.pdf*")


