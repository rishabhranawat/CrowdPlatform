from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator

es = Elasticsearch()

class SearchES:
    
    def add_relevant_terms_mapping(self, s, relevant_terms):
        for term in relevant_terms:
            ts = term.split(",")
            for each in ts:
                mod_term = "*"+each.replace(" ", "?").lower()+"*"
                s.add_bool_condition("should", "wildcard", "content", mod_term)
        return
    
    def generate_relevant_query_maps(self, relevant_terms, phase):
        search_mappings = []
         
        if(phase==1):
            
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms)
            s.add_bool_condition("must", "wildcard", "link", "*wikipedia*")
            s.add_bool_condition("must_not", "wildcard", "link", "*edit*")
            s.add_bool_condition("must_not", "wildcard", "link", "*&oldid*")
            search_mappings.append((s.body, 5))
           
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms) 
            s.add_bool_condition("must_not", "wildcard", "link", "*wikipedia*")
            s.add_bool_condition("must", "wildcard", "link", "*edu*")
            search_mappings.append((s.body, 5))
            
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms)            

            s.add_bool_condition("must_not", "wildcard", "link", "*wikipedia*")
            s.add_bool_condition("must_not", "wildcard", "link", "*edu*")
            search_mappings.append((s.body, 5)) 
        else:
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms)
            s.add_bool_condition("must", "wildcard", "link", "*homework*")
            search_mappings.append((s.body, 5))
            
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms)
            s.add_bool_condition("must", "wildcard", "link", "*midterm*")
            search_mappings.append((s.body, 5))
                
            s = SearchMappingGenerator()
            self.add_relevant_terms_mapping(s, relevant_terms)
            s.add_bool_condition("must", "wildcard", "link", "*final*")
            search_mappings.append((s.body, 5))
        return search_mappings

    def generate_search_urls(self, relevant_terms, phase=1):
        mappings = self.generate_relevant_query_maps(relevant_terms, phase)
        links = set()
        for mapping in mappings:
            results = es.search(index="offline_content", body=mapping[0], size=mapping[1])
            print(results["hits"]["total"])
            for hit in results["hits"]["hits"]:
                link = hit["_source"]["link"]
                score = hit["_score"]
                links.add(link)
        return links
