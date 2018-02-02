import requests
from collections import Counter

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

import networkx as nx
        
path = "../graph_query/graphs/knowledge_graph.gpickle" 
kg = nx.read_gpickle(path)
kg_labels = [str(x) for x in list(kg.nodes())[1:]]


def get_tfd(content):
	word_count_dict = Counter(w for w in kg_labels if w.lower() in content.lower())
	arr = [0]*len(kg_labels)
	common = word_count_dict.most_common()

	for each in common:

		ind = kg_labels.index(each[0])
		arr[ind] = each[1]

	print(arr)
	return arr

def get_coocc_matrix(docs):
	pass



def get_significance_score(docs):
	pass

def get_relationship_score(docs):
	pass

def get_content():
	f = open('sample_urls.txt', 'r')
	l = f.readlines()
	docs = {}
	index = {}

	counter = 0
	for each in l:
		docs[each] = requests.get(each).content
		index[each] = counter
		counter += 1
	return docs, index

if __name__ == "__main__":

	content, index = get_content()

	# docs = [content1, content2]

	tfd_data = {'TFD':[1:len()]}
	for url, cont in content.items():
		tfd_data[index[url]] = get_tfd(cont)


	df = pd.DataFrame(tfd_data).set_index('TFD')
	df_asint = df.astype(int)
	coocc = df_asint.T.dot(df_asint)
	print(coocc[0][0])
