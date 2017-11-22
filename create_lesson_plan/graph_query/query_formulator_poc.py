# ### Graph Query Formulator
# Exploring the idea of generating optimal queries for elasticsearch using a graph datastructure that contains the ontologies of different courses and thus, acts like a knowledge graph.

import pickle
import json

import networkx as nx
import nltk

class GraphQueryFormulator:
	def __init__(self):
		self.kg = nx.read_gpickle("create_lesson_plan/graph_query/ml_graph.gpickle")

        '''
        To interface with the module
        '''
	def get_queries(self, query):
		return self.query_formulator(query)	
		
	'''
        Closest edit distance.
        args - query (str)
        TODO: Sent2Vec
        '''
        def get_closest_distance_node(self, query):
	    nodes = self.kg.nodes()
	    mi, val = None, None
	    for node in nodes:
		dist = nltk.distance.edit_distance(node, query)
		if(mi == None or dist < mi): 
		    mi = dist
		    val = node
		if(query in node 
                        and (self.kg.node[node]["NodeType"] == "ConceptNode" 
                            or query not in val)): 
		    return node
	    return val

        '''
        Returns the node with the minimum edit distance.
        args - query (str)
        returns - label of closest node (str), closest node (nx.node)
        '''
	def get_closest_node(self, query):
	    if(query in self.kg.nodes()): 
		return query, self.kg.node[query]
	    else: 
		node_label = self.get_closest_distance_node(query)
		return node_label, self.kg.node[node_label]

        def get_queries_based_on_node(self, node_label):
            node = self.kg.node[node_label]
            node_type = node["NodeType"]
            
            if(node_type == "TopicNode" or node_type == "ConceptNode"):
                return self.kg.neighbors(node_label)
            elif(node_type == "ConceptNode"):
                return self.kg.neighbors(node_label)
            elif(node_type == "SubConceptNode"):
                return [node_label]
            else:
                pass


        '''
        Returns a list of queries depending on the type of the
        node closest to the query.
        args - query(str)
        returns [] of str
        '''
	def query_formulator(self, query):
	    queries = []
	    node_label, node = self.get_closest_node(query)
            children_neighbours = self.get_queries_based_on_node(node_label)

	    print(node_label, node, children_neighbours)
	    for child in children_neighbours:
			queries.append(node_label+" "+child)
	    return queries

