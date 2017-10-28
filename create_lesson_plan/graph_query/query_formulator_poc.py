
# coding: utf-8

# ### Graph Query Formulator
# Exploring the idea of generating optimal queries for elasticsearch using a graph datastructure that contains the ontologies of different courses and thus, acts like a knowledge graph.

import pickle
import json

import networkx as nx
import nltk

class GraphQueryFormulator:
	def __init__(self):
		pass
	
	def get_queries(self, query):
		kg = nx.read_gpickle("create_lesson_plan/graph_query/algorithms.gpickle")
		return self.query_formulator(kg, query)	
		
	def get_closest_distance_node(self, query, kg):
	    nodes = kg.nodes()
	    mi, val = None, None
	    for node in nodes:
		dist = nltk.distance.edit_distance(node, query)
		if(mi == None or dist < mi): 
		    mi = dist
		    val = node
		if(query in node and (kg.node[node]["NodeType"] == "ConceptNode" or query not in val)): 
		    return node
	    return val

	def get_closest_node(self, query, kg):
	    if(query in kg.nodes()): 
		return query, kg.node[query]
	    else: 
		node_label = self.get_closest_distance_node(query, kg)
		return node_label, kg.node[node_label]

	def query_formulator(self, kg, query):
	    print(query)
	    queries = []
	    current_node, node = self.get_closest_node(query, kg)
	    children_neighbours = kg.neighbors(current_node)
	    
	    print(current_node, node, children_neighbours)
	    for child in children_neighbours:
		queries.append(current_node+" "+child)
	    return queries

