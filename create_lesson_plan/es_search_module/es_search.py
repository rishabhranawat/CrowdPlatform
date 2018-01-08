import requests
import time

from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator
from create_lesson_plan.dups_detector import DuplicateDetector

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


class SearchES:
	
	def __init__(self):
		self.dups_detector = DuplicateDetector()

	def add_relevant_terms_mapping(self, s, relevant_terms, query):
		print(query, relevant_terms)
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

	def detect_dups(self, details):
                start = time.time()
		content = []
                links = []
		for dets in details:
			content.append(dets[1])
			links.append(dets[0])

		dup_sets = []
		for i in range(0, len(links), 1):
			per_dup_set = [links[i]]
			for j in range(0, len(links), 1):
				if(i == j): continue
				if(self.dups_detector.detect(content[i], content[j]) > 0.7):
					per_dup_set.append(links[j])
			dup_sets.append(per_dup_set)

		absolute_unique_links = set()
		for per in dup_sets:
			absolute_unique_links.add(per[0])
		print("DETECT DUPS", absolute_unique_links)
		print("time taken for duplicate", time.time()-start)
                return absolute_unique_links



	def generate_search_urls(self, relevant_terms, phase=1):
		query, relevant_terms = relevant_terms[0], relevant_terms[1:]
		mappings = self.generate_relevant_query_maps(query, relevant_terms, phase)
		links = set()
                
                start = time.time()
		p = Pool(4)
		results = list(p.imap_unordered(execute_query_get_results, mappings))
		p.close()
		p.join()
		
                print("Time taken to get", time.time()-start)
                collated_results = [item[0] for sublist in results for item in sublist]
		return list(collated_results)
