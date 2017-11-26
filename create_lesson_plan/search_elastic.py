from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from graph_query.query_formulator_poc import GraphQueryFormulator


client = Elasticsearch()

class ElasticsearchOfflineDocuments():
	def __init__(self):
		self.gqf = GraphQueryFormulator()

	def get_query_lesson_outline(self, lesson_outline):
		q_lesson_outline = []
		for bullet in lesson_outline:
                    print(bullet)
                    q_lesson_outline.append(Q("match", content=bullet))
		q_outlines = Q('bool', should=q_lesson_outline, minimum_should_match=1)
		return q_outlines		

	def get_required_links(self, hits):
		links = []
		for hit in hits:
			if("syllabus" not in str(hit.link)): links.append(hit.link)
		return set(links)

        def get_diversity_links(self, phase):
                if(phase == 1):
                    q_wiki = Q("wildcard", link="*wikipedia*")
                    q_edu = Q("wildcard", link="*\.edu*")
                    q_edu_pdf = Q("wildcard", link="*.pdf*")
                    q_random = ~q_wiki & ~q_edu

                    query_types= [(q_wiki, 4), (q_edu, 5), (q_random, 5)]
                    return query_types
                else:
                    print('here1')
                    q_link_m = Q("wildcard", link="*midterm*")
                    q_link_e = Q("wildcard", link="*exam*")
                    q_link_f = Q("wildcard", link="*final*")
                    q_link_s = Q("wildcard", link="*solutions*")
                    q_link_hw = Q("wildcard", link="*hw*")
                    q_link_h = Q("wildcard", link="*homework*")

                    q_link = q_link_m or q_link_e or q_link_f or q_link_s \
                            or q_link_hw or q_link_h
                    return [(q_link, 20)]

	def generate_search_urls(self, input_title, lesson_outline, phase=1, source=""):
		s = Search(using=client, index="offline_content")
		lesson_outline_q = self.get_query_lesson_outline(lesson_outline)
                print(lesson_outline)
		results = set()
		query_types = self.get_diversity_links(phase)
                for each_type in query_types:
		    query = lesson_outline_q & each_type[0]
		    res = s.query(query)[:each_type[1]]
		    hits = res.execute()
		    results |= self.get_required_links(hits)

		return results

	def get_graph_based_queries(self, query):
		queries = self.gqf.get_queries(query)
                if(len(queries) == 0): return [query]
                else: return queries
