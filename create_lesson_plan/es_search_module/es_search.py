from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator

es = Elasticsearch()

class SearchES:
    
    def add_relevant_terms_mapping(self, s, relevant_terms, query):
        s.add_bool_condition("must", "match_phrase", "content", "*"+query+"*")
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
            
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms, query)
            s.add_bool_condition("must", "wildcard", "link", "*wikipedia*")
            s.add_bool_condition("must_not", "wildcard", "link", "*edit*")
            s.add_bool_condition("must_not", "wildcard", "link", "*&oldid*")
            search_mappings.append((s.body, 20))
           
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms, query) 
            s.add_bool_condition("must_not", "wildcard", "link", "*wikipedia*")
            s.add_bool_condition("must", "wildcard", "link", "*edu*")
            search_mappings.append((s.body, 5))
            
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms, query)            
            s.add_bool_condition("must_not", "wildcard", "link", "*wikipedia*")
            s.add_bool_condition("must_not", "wildcard", "link", "*edu*")
            search_mappings.append((s.body, 5)) 
        
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

    def generate_search_urls(self, relevant_terms, phase=1):
        query, relevant_terms = relevant_terms[0], relevant_terms[1:]
        mappings = self.generate_relevant_query_maps(query, relevant_terms, phase)
        links = set()
        for mapping in mappings:
            results = es.search(index="offline_content", body=mapping[0], size=mapping[1])
            print(results["hits"]["total"])
            for hit in results["hits"]["hits"]:
                link = hit["_source"]["link"]
                score = hit["_score"]
                print(score, link)
                links.add(link)
        return links
