import pickle
import json

import networkx as nx
import nltk

class GraphQueryFormulator:
	def __init__(self):
                self.path = "create_lesson_plan/graph_query/graphs/knowledge_graph.gpickle" 
		self.kg = nx.read_gpickle(self.path)

        def add_to_kg(self, closest_node_label, query):
            closest_node=self.kg.node[closest_node_label]
            if("NodeType" not in closest_node):
                self.kg.add_node(query, NodeType="ConceptNode") 
            elif(closest_node["NodeType"] == "TopicNode"):
                self.kg.add_node(query, NodeType="ConceptNode")
                self.kg.add_edges_from([(closest_node_label, query)])
            elif(closest_node["NodeType"] == "ConceptNode"):
                self.kg.add_node(query, NodeType="ConceptNode")
                print(list(self.kg.predecessors(closest_node_label))[0])
                self.kg.add_edges_from([(list(self.kg.predecessors(closest_node_label))[0], query)])
            nx.write_gpickle(self.kg, self.path)
            self.kg = nx.read_gpickle(self.path)            
        '''
        To interface with the module
        '''
	def get_queries(self, query, label):
		return self.query_formulator(query, label)	
		
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
		if(query in node and (self.kg.node[node]["NodeType"] == "ConceptNode" 
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
			return list(self.kg.neighbors(node_label))
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
	def query_formulator(self, query, label):
	    queries = []
	    #node_label, node = label, self.kg.node[label]
            print(label)
	    children_neighbours = self.get_queries_based_on_node(label)
	    queries = [label]
            for child in children_neighbours:
			queries.append(child)
            print(queries)
	    return queries

