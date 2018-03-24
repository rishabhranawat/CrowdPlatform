import requests
import time

from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator
from create_lesson_plan.dups_detector import DuplicateDetector
from create_lesson_plan.simhash_dups import Simhash, SimhashIndex
from create_lesson_plan.comprehension_burden_module.comprehension_burden import LP, CB

from multiprocessing import Pool
from functools import partial

es = Elasticsearch()

def execute_query_get_results(mapping):
		links = set()
		results = es.search(index="offline_content", body=mapping[0], size=mapping[1])
		for hit in results["hits"]["hits"]:
			link = hit["_source"]["link"]
			score = hit["_score"]
			content = hit["_source"]["content"]
			if("content" in hit["_source"]["attachment"]):
				content = hit["_source"]["attachment"]["content"]
			links.add((link, content))
		return links

def get_simhash(kv):
	k, v = kv[0], kv[1]
	return (str(k), Simhash(v))

class SearchES:
	
	def __init__(self):
		self.dups_detector = DuplicateDetector()

	def add_relevant_terms_mapping(self, s, relevant_terms, query):
		s.add_bool_condition("must", "match_phrase", "content", "*"+query.lower()+"*")
		for term in relevant_terms:
			ts = term.split(",")
			for each in ts:
				mod_term = "*"+each+"*"
				s.add_bool_condition("should", "match_phrase", "content", mod_term)
		return
	
	def add_relevant_evaluate_mapping(self, s):
		typs = ["homework", "problems", "final", "midterm", "solution"]
		for term in typs:
			s.add_bool_condition("should", "match_phrase", "content", term)
		return
	
	def generate_relevant_query_maps(self, query, relevant_terms, phase):
		search_mappings = []
		 
		if(phase==1):    
			s1 = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s1, relevant_terms, query)
			s1.add_bool_condition("must", "wildcard", "link", "*wikipedia*")
			s1.add_bool_condition("must_not", "wildcard", "link", "*edit*")
			s1.add_bool_condition("must_not", "wildcard", "link", "*&oldid*")
			search_mappings.append((s1.body, 5))
		   
			s2 = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s2, relevant_terms, query) 
			s2.add_bool_condition("must_not", "wildcard", "link", "*wikipedia*")
			s2.add_bool_condition("must", "wildcard", "link", "*edu*")
			search_mappings.append((s2.body, 5))
			
			s3 = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s3, relevant_terms, query)            
			s3.add_bool_condition("must_not", "wildcard", "link", "*wikipedia*")
			s3.add_bool_condition("must_not", "wildcard", "link", "*edu*")
			search_mappings.append((s3.body, 10)) 

			s4 = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s4, relevant_terms, query)
			s4.add_bool_condition("must", "wildcard", "link", "*.pdf*")
			search_mappings.append((s4.body, 5))
		
		else:
			s = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s, relevant_terms, query)
			s.add_bool_condition("should", "wildcard", "link", "*hw*")
			s.add_bool_condition("should", "wildcard", "link", "*homework*")
			self.add_relevant_evaluate_mapping(s)
			search_mappings.append((s.body, 5))
			
			s = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s, relevant_terms, query)
			s.add_bool_condition("must", "wildcard", "link", "*midterm*")
			self.add_relevant_evaluate_mapping(s)
			search_mappings.append((s.body, 5))
				
			s = SearchMappingGenerator()
			self.add_relevant_terms_mapping(s, relevant_terms, query)
			s.add_bool_condition("must", "wildcard", "link", "*final*")
			self.add_relevant_evaluate_mapping(s)
			search_mappings.append((s.body, 5))

		return search_mappings

	def simhash_detect_dups(self, details):
		links = {}
		cont = {}

		for i in range(0, len(details)):
			links[i] = details[i][0]
			cont[i] = details[i][1]
                
        objs = [(str(k), Simhash(v)) for k, v in cont.items()]
		index = SimhashIndex(objs, k=5)
		visited = set()

		all_dups_sets = []
		for ind, content in cont.items():
			if(ind not in visited):
				test_data = Simhash(content)
				dups = index.get_near_dups(test_data)
				all_dups_sets.append(dups)
				for each in dups: visited.add(int(ind))

		absolute_unique_links = set()
		for each in all_dups_sets:
			absolute_unique_links.add(links[int(each[0])])
		return absolute_unique_links

	def sequence_links(self, details, unique_links):
		docs = {}
		index = {}
		counter = 0
		links_to_cont = {}
		for i in range(0, len(details), 1):
			l = details[i][0]
			if(l in unique_links and l not in index):
				docs[l] = details[i][1]
				index[l] = counter
				counter += 1
		lp = LP(docs, index)
		cb = CB(lp)
		sequence, doc_to_keys = cb.get_cb(2, "linearWeighted", "alphabetical")
		return sequence, doc_to_keys


	def generate_search_urls(self, relevant_terms, phase=1):
		query, relevant_terms = relevant_terms[0], relevant_terms[1:]
		mappings = self.generate_relevant_query_maps(query, relevant_terms, phase)
		links = set()
				
		p = Pool(4)
		results = list(p.imap_unordered(execute_query_get_results, mappings))
		p.close()
		p.join()
		
		collated_results = [item for sublist in results for item in sublist]
		unique_results = self.simhash_detect_dups(list(collated_results))
		sequenced, doc_to_keys = self.sequence_links(list(collated_results), unique_results)
		return sequenced, doc_to_keys
