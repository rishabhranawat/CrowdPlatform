import networkx as nx
import json

from networkx.readwrite import json_graph

class GraphView:

	def find_root(self, graph):
		nodes = graph.nodes
		for each in nodes:
			if(len(list(graph.predecessors(each))) == 0):
				return each
		return nodes[0]

	def generate(self, kg, tags):

		graph = kg.subgraph(tags)

		root = self.find_root(graph)
		dfs_tree = list(nx.dfs_tree(graph).edges())


		treeData = []
		for pair in dfs_tree:
			parent = pair[0]
			child = pair[1]
			

tags = [u'Linear Programming',
 u'Files',
 u'Duality',
 u'Pca',
 u'Processes',
 u'Unsupervised Learning',
 u'Deep Learning',
 u'Clustering',
 u'Noise',
 u'Linear Regression',
 u'Bias',
 u'Convex Optimization',
 u'Iteration',
 u'Dfs',
 u'Portfolio Optimization',
 u'Regression',
 u'Scheduling',
 u'Variance']

path = "graph_query/graphs/knowledge_graph.gpickle" 
kg = nx.read_gpickle(path)

sub = kg.subgraph(tags)

d = json_graph.node_link_data(sub)
json.dump(d, open('../kg_json_dump.json','w'))





