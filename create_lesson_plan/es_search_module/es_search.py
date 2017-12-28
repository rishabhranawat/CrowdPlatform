from elasticsearch import Elasticsearch
from mapping_generator import SearchMappingGenerator

es = Elasticsearch()

class SearchES:
    
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
            search_mappings.append(s4, 5)
        
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
            print(phase, mapping, query)
            results = es.search(index="offline_content", body=mapping[0], size=mapping[1])
            print(results["hits"]["total"])
            for hit in results["hits"]["hits"]:
                link = hit["_source"]["link"]
                score = hit["_score"]
                print(score, link)
                links.add(link)
        return links
