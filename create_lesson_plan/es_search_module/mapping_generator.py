import json

class SearchMappingGenerator:
    
    def __init__(self):
        self.body = {
            "query":{
                "bool":{
                    "must_not":[],
                    "must":[],
                    "should":[]
                }
            }
        }

   
    def replace_map(self, body):
        self.body = body    

    def add_bool_condition(self, condition_type, match_type, field, value):
        mapping = {match_type:{field:value}}
        self.body["query"]["bool"][condition_type].append(mapping)
        return True
    
    def edit_minimum_should_number(self, number):
        self.body["query"]["bool"]["minimum_should_match"] = number
