import networkx as nx

kg = nx.read_gpickle("../create_lesson_plan/graph_query/graphs/knowledge_graph.gpickle")

f = open("kg_nodes.txt", "w")
for each in kg.nodes():
    f.write(each+"\n")
f.close()
