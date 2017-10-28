import json
import pickle

import networkx as nx


G = nx.Graph()
G.add_node('Algorithms')
G.add_edge('Algorithms', 'Problems')