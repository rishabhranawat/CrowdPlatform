
# coding: utf-8

# ### Graph Query Formulator
# Exploring the idea of generating optimal queries for elasticsearch using a graph datastructure that contains the ontologies of different courses and thus, acts like a knowledge graph.

import pickle
import json

import networkx as nx
import nltk

class GraphQueryFormulator:
	def __init__(self):
		self.kg = nx.read_gpickle("create_lesson_plan/graph_query/algorithms.gpickle")
	
	def get_queries(self, query):
		return self.query_formulator(query)	
		
	def get_closest_distance_node(self, query):
	    nodes = self.kg.nodes()
	    mi, val = None, None
	    for node in nodes:
		dist = nltk.distance.edit_distance(node, query)
		if(mi == None or dist < mi): 
		    mi = dist
		    val = node
		if(query in node and (self.kg.node[node]["NodeType"] == "ConceptNode" or query not in val)): 
		    return node
	    return val

	def get_closest_node(self, query):
	    if(query in self.kg.nodes()): 
		return query, self.kg.node[query]
	    else: 
		node_label = self.get_closest_distance_node(query)
		return node_label, self.kg.node[node_label]

	def query_formulator(self, query):
	    print(query)
	    queries = []
	    current_node, node = self.get_closest_node(query)
	    children_neighbours = self.kg.neighbors(current_node)
	    
	    print(current_node, node, children_neighbours)
	    for child in children_neighbours:
			queries.append(current_node+" "+child)
	    print(queries)
	    return queries

