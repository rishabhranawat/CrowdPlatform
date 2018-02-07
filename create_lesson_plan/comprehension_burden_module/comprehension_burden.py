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
		if(counter == 2):
			break
	return docs, index

if __name__ == "__main__":

	content, index = get_content()

	tfd_data = {}
	for url, cont in content.items():
		tfd_data[url] = get_tfd(cont)

	tfd_arr = [0]*len(index)
	for i in range(0, len(tfd_arr),1):
		tfd_arr[i] = i
	word_data = {'TFD':tfd_arr}

	for each in kg_labels:
		word_data[each] = [0]*len(index)
	
	for url, words_in_doc in tfd_data.items():
		ind = index[url]
		for i in range(0, len(words_in_doc), 1):
			word = kg_labels[i]
			word_data[word][ind] = words_in_doc[i]
		
	df = pd.DataFrame(word_data).set_index('TFD')
	df_asint = df.astype(int)
	print(df_asint.iloc[0])



