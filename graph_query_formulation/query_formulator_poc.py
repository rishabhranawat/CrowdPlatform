
# coding: utf-8

# ### Graph Query Formulator
# Exploring the idea of generating optimal queries for elasticsearch using a graph datastructure that contains the ontologies of different courses and thus, acts like a knowledge graph.

import pickle
import json

import networkx as nx
import nltk

def get_closest_distance_node(query, kg):
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

def get_closest_node(query, kg):
    if(query in kg): 
        return query, kg.node[query]
    else: 
        node_label = get_closest_distance_node(query, kg)
        return node_label, kg.node[node_label]


def query_formulator(kg, query):
    queries = []
    current_node, node = get_closest_node(query, kg)
    children_neighbours = kg.neighbors(current_node)
    pr = nx.pagerank(kg, alpha=0.9)
    for child in children_neighbours:
        queries.append(current_node+" "+child)
    return queries

kg = nx.read_gpickle("graphs/algorithms.gpickle")
print(query_formulator(kg, "sorting"))




