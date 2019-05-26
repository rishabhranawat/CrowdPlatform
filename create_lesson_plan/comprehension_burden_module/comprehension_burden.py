import requests
from collections import Counter
import random as randomlib
import logging

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import networkx as nx

import itertools
import pickle
import operator

'''
Lesson Plan Object
'''
class LP:
	def __init__(self, filepath):
		self.content, self.index = self.get_lpd(filepath)
		self.number_of_docs = len(self.content)

	# def __init__(self, docs, index):
	#     self.content, self.index = docs, index

	def get_lpd(self, filepath):
		f = open(filepath, 'r')
		l = f.readlines()
		docs = {}
		index = {}
		counter = 0

		logging.info("Fetching content for documents")
		for u in l:
			url = u.replace("\n", "")
			try:
				docs[url] = requests.get(url).content
				index[url] = counter
				counter += 1
			except:
				print(url, "Error")
				continue
		f.close()
		logging.info("Completed content for documents")
		return docs, index

class ConceptDetails:
	def __init__(self, label, typ, score):
		self.label = label
		self.type = typ
		self.score = score

	def __lt__(self, other):
		return self.score < other.score

	def __le__(self, other):
		return self.score <= other.score

	def __eq__(self, other):
		return self.score == other.score

	def __ne__(self, other):
		return self.score != other.score

	def __gt__(self, other):
		return self.score > other.score

	def __ge__(self, other):
		return self.score >= other.score

	def __str__(self):
		return "label: "+self.label + " score: "+str(self.score)\
		+" type: "+self.type

class GraphNode:
	def __init__(self, label):
		self.label = label
		self.neighbors = []

	def __str__(self):
		return self.label

class SequenceGenerator:

	def __init__(self, kg, nodes, concept_to_score):
		self.kg = kg
		self.nodes = nodes
		self.graph = self.create_graph()
		self.concept_to_score = concept_to_score

	def create_graph(self):
		label_node = {}

		# GraphNode for each node
		for each in self.nodes:
			gNode = GraphNode(each)
			label_node[each] = gNode

		# Neighbours
		for each in self.nodes:
			gn = label_node[each]
			for ne in self.kg.neighbors(each):
				if(ne in label_node):
					gn.neighbors.append(label_node[ne])
		
		graph = []
		for each in self.nodes:
			graph.append(label_node[each])
		return graph

	def get_bfs_sequence(self):
		visited = set()
		sequence = []
		for each in self.graph:
			if(each in visited): continue
			queue = [each]
			while(queue):
				n = queue.pop(0)
				sequence.append(n.label)
				visited.add(n)
				if(n in visited): continue
				else:
					for c in n.neighbors:
						if(c not in queue and c not in visited):
							queue.append(c)
		return sequence

	def dfs(self, node, visited, sequence):
		if(node in visited): return
		else:
			visited.append(node)
			sequence.append(node.label)
			for each in node.neighbors:
				if(each not in visited):
					self.dfs(each, visited, sequence)
	
	def get_dfs_sequence(self):
		visited = []
		sequence = []
		for node in self.graph:
			self.dfs(node, visited, sequence)
		return sequence

	def get_linear_weighted_sequence(self):
		parents = []
		for each in self.nodes:
			if(each in self.kg.nodes 
				and self.kg.nodes[each]["NodeType"] == "TopicNode"):
				parents.append(each)
		scored_parents = [(pa, self.concept_to_score[pa]) for pa in parents]
		scored_parents.sort(key=lambda x:x[1], reverse=True)

		
		linear = []
		for p, s in scored_parents:
			linear.append(p)
			
			scored_children = []
			for child in self.kg.neighbors(p):
				if(child in self.concept_to_score):
					scored_children.append((child, self.concept_to_score[child]))
			scored_children.sort(key=lambda x:x[1],  reverse=True)
			for c, s in scored_children:
				if c in self.nodes \
				and self.kg.nodes[c]["NodeType"] == "ConceptNode":
					linear.append(c)
		
		for each in self.nodes:
			if each not in linear:
				linear.append(each)
		
		return linear		

	def get_linear_sequence(self):
		parents = []
		for each in self.nodes:
			if(each in self.kg.nodes and self.kg.nodes[each]["NodeType"] == "TopicNode"):
				parents.append(each)
		
		linear = []
		for p in parents:
			linear.append(p)
			children = self.kg.neighbors(p)
			for c in children:
				if c in self.nodes and self.kg.nodes[c]["NodeType"] == "ConceptNode":
					linear.append(c)
		
		for each in self.nodes:
			if each not in linear:
				linear.append(each)
		
		return linear

	def get_lws(self, prev, current_label, sequence):
		if(len(prev) == 0): return
		new_prev = []
		for p in prev:
			if(p not in sequence):
				sequence.append(p)

				for c in self.kg.neighbors(p):
					if(c in self.nodes and self.kg.nodes[c]["NodeType"] == current_label):
						new_prev.append(c)
						sequence.append(c)
		for each in new_prev:
			self.get_lws(new_prev, "SubConceptNode", sequence)

	def start(self):
		prev = []
		for each in self.nodes:
			if(each in self.kg.nodes 
				and self.kg.nodes[each]["NodeType"] == "TopicNode"):
				prev.append(each)
		sequence = []
		self.get_lws(prev, "ConceptNode", sequence)

		for each in self.nodes:
			if each not in sequence:
				sequence.append(each)
			
		return sequence

	def get_base_sequence(self):
		return self.nodes

	def get_random_sequence(self):
		vals = list(self.nodes)
		r = []
		while(vals):
			s = randomlib.choice(vals)
			r.append(s)
			vals.remove(s)
		return r

	def documents_with_concept(self, doc_to_concepts, concept):
		docs = []
		for k, v in doc_to_concepts.items():
			for doc_c in v:
				if(doc_c == concept):
					return k
		return None

	def arrange_docs(self, sequence, doc_to_keys):
		docs_sequence = []
		for each_con in sequence:
			related_doc = self.documents_with_concept(doc_to_keys, each_con)
			if(related_doc != None):
				docs_sequence.append(related_doc)
		return docs_sequence



class CB:
	def __init__(self, LP):
		self.kg_labels, self.kg = self.get_kg_labels()
		self.lp = LP
		self.document_term_frequency, self.dtf_asint, self.coocc = self.get_matrices()

	'''
	Get kg labels
	'''
	def get_kg_labels(self):
		kg_path = "../graph_query/graphs/weighted_knowledge_graph.gpickle"
		kg = nx.read_gpickle(kg_path)
		return [str(x) for x in list(kg.nodes())[1:]], kg

	'''
	Term Frequency Array for a particular document
	Returns arr[index matches kg_labels] = freq
	'''
	def get_tfd(self, document):
		word_count_dict = Counter(w for w in self.kg_labels 
								  if w.lower() in document.lower())
		common = word_count_dict.most_common()
		
		frequency_arr = [0]*len(self.kg_labels)
		
		for common_word in common:
			common_word_index = self.kg_labels.index(common_word[0])
			frequency_arr[common_word_index] = common_word[1]
		return frequency_arr

	'''
	Matrices for a given LP
	Document Term Frequency, Document Term Frequency as int
	and Coocurence.
	'''
	def get_matrices(self):
		tfd_data = {}
		for url, cont in self.lp.content.items():
			tfd_data[url] = self.get_tfd(cont)

		tfd_arr = []
		for key in self.lp.index.keys():
			tfd_arr.append(key)

		word_data = {'TFD':tfd_arr}
		for label in self.kg_labels:
			word_data[label] = [None]*len(self.lp.index)

		for url, words_in_doc in tfd_data.items():
			url_index = self.lp.index[url]
			for i in range(0, len(self.kg_labels), 1):
				word = self.kg_labels[i]
				word_data[word][url_index] = words_in_doc[i]

		document_term_frequency = pd.DataFrame(word_data).set_index('TFD')
		dtf_asint = document_term_frequency.astype(int)
		coocc = dtf_asint.T.dot(dtf_asint)

		return document_term_frequency, dtf_asint, coocc

	'''
	Relationship between concepts: Co occurence score
	'''
	def get_relationship_between_concepts(self, concept_1, concept_2):
		concept_1_index= self.document_term_frequency.columns.get_loc(concept_1)
		concept_2_index= self.document_term_frequency.columns.get_loc(concept_2)
		
		return self.coocc.iloc[concept_1_index, concept_2_index]
	
	'''
	Significance Score of a given concept in a particular document
	score = frequency of concept in document + |Related concept|
	'''
	def get_significance_score(self, concept, document):
		concept_index = self.document_term_frequency.columns.get_loc(concept)
		freq = self.dtf_asint.iloc[self.lp.index[document]][concept_index]
		coocc_row = np.array(self.coocc.iloc[concept_index,:])
		return freq*np.count_nonzero(coocc_row)	

	'''
	Finding Document to top(N) Key Sections mapping
	'''
	def documents_with_concept(self, doc_to_concepts, concept):
		docs = []
		for k, v in doc_to_concepts.items():
			for doc_c in v:
				if(doc_c.label == concept):
					docs.append(k)
					break
		return docs

	def assign_key_concepts(self, top_n, doc_to_concepts, concepts, topics):
		doc_to_keys = {}
		relevant_concepts = set()
		for k, v in doc_to_concepts.items():
			doc_to_keys[k] = []

		for each_concept in concepts:
			relevant_docs = self.documents_with_concept(doc_to_concepts, 
				each_concept)
			relevant_docs.sort(key=lambda x:x[1], reverse=True)

			for each_doc in relevant_docs:
				if(len(doc_to_keys[each_doc]) < top_n):
					doc_to_keys[each_doc].append(each_concept)
					relevant_concepts.add(each_concept)
					break

		for each_topic in topics:
			relevant_docs = self.documents_with_concept(doc_to_concepts, 
				each_topic)
			relevant_docs.sort(key=lambda x:x[1], reverse=True)

			for each_doc in relevant_docs:
				if(len(doc_to_keys[each_doc]) < top_n):
					doc_to_keys[each_doc].append(each_topic)
					relevant_concepts.add(each_topic)
					break
		return doc_to_keys, relevant_concepts

	def get_doc_to_key_concepts(self, top_n):
		doc_to_concepts = {}

		all_topics = set()
		all_concepts = set()
		for each_document in self.lp.content.keys():
			rt = []
			rc = []

			for each_concept in self.kg_labels:

				s = self.get_significance_score(each_concept, each_document)
				if(s <= 0): continue
				if("NodeType" not in self.kg.node[each_concept]): continue
				elif(self.kg.node[each_concept]["NodeType"] == "ConceptNode"):
					rc.append(ConceptDetails(each_concept, "ConceptNode", s))
					all_concepts.add(each_concept)
				elif(self.kg.node[each_concept]["NodeType"] == "TopicNode"):
					rt.append(ConceptDetails(each_concept, "TopicNode", s))
					all_topics.add(each_concept)

			sorted(rt, reverse=True)
			sorted(rc, reverse=True)
			rc.extend(rt)
			doc_to_concepts[each_document] = rc
		a, b = self.assign_key_concepts(top_n, doc_to_concepts, all_concepts, 
		all_topics)
		return doc_to_concepts, a, b

	'''
	Computing Comprehension Burden
	'''
	def document_cb(self, document, related_concepts, key_concepts, visited):
		document_burden = 0.0
		count = 0
		for rel in related_concepts:
			related_c = rel.label
			burden = 0.0
			if(related_c not in visited):
				for key_c in key_concepts:
					count += 1
					burden += self.get_significance_score(related_c, document)
			if(count > 0): 
				document_burden += burden/count
		return document_burden

	'''
	Get collective burden for a lesson plan
	'''
	def lp_cb(self, sequenced, doc_to_concepts, doc_to_keys):
		visited = set()
		collective_burden = 0.0

		for d in sequenced:
			for d_keys in doc_to_keys[d]:
				visited.add(d_keys)

			burden = self.document_cb(d, doc_to_concepts[d], doc_to_keys[d], visited)
			collective_burden += burden

		return collective_burden

	def get_cb_for_sequence(self, typ, s, doc_to_concepts, doc_to_keys):
		docs_sequence = []
		if(typ == "linear"):
			linear_sequence = s.get_linear_sequence()
			print("linear", linear_sequence)
			docs_sequence = s.arrange_docs(linear_sequence, doc_to_keys)
		elif("random" in typ):
			random_sequence = s.get_random_sequence()
			docs_sequence = s.arrange_docs(random_sequence, doc_to_keys)
		elif(typ == "bfs"):
			bfs_sequence = s.get_bfs_sequence()
			# print('bfs', bfs_sequence)
			docs_sequence = s.arrange_docs(bfs_sequence, doc_to_keys)
		elif(typ == "dfs"):
			dfs_sequence = s.get_dfs_sequence()
			docs_sequence = s.arrange_docs(dfs_sequence, doc_to_keys)
		elif(typ == "base"):
			base_sequence = s.get_base_sequence()
			docs_sequence = s.arrange_docs(base_sequence, doc_to_keys)
		elif(typ == "linearWeighted"):
			linear_weighted_sequence = s.get_linear_weighted_sequence()
			print('weighted', linear_weighted_sequence)
			docs_sequence =  s.arrange_docs(linear_weighted_sequence, doc_to_keys)
		elif(typ == "start"):
			start = s.start()

		return self.lp_cb(docs_sequence, doc_to_concepts, doc_to_keys)

	def get_base_arrangement(self, related_concepts, concept_to_score, typ):
		if(typ == "alphabetical"):
			return sorted(list(related_concepts))
		elif(typ == "maximizer"):
			sorted_concept_to_score = sorted(concept_to_score.items(), key=operator.itemgetter(1), reverse=True)
			return [x[0] for x in sorted_concept_to_score]
		elif("random" in typ):
			vals = list(related_concepts)
			r = []
			while(vals):
				s = randomlib.choice(vals)
				r.append(s)
				vals.remove(s)
			return r

	def get_concept_to_global_score(self, related_concepts, doc_to_keys):
		concept_to_score = {}
		for each_concept in related_concepts:
			concept_score = 0.0
			for each_document in doc_to_keys.keys():
				concept_score += self.get_significance_score(each_concept, each_document)
			concept_to_score[each_concept] = concept_score
		return concept_to_score


	def get_cb(self, top_n, typ, base_arrangement):
		doc_to_concepts, doc_to_keys, related_concepts = self.get_doc_to_key_concepts(top_n)

		concept_to_score = self.get_concept_to_global_score(related_concepts, doc_to_keys)
		print(doc_to_keys)
		related_concepts = self.get_base_arrangement(related_concepts, concept_to_score, base_arrangement)
		s = SequenceGenerator(self.kg, related_concepts, concept_to_score)
		return self.get_cb_for_sequence(typ, s, doc_to_concepts, doc_to_keys)

	def get_sequenced_documents_present(self, top_n, typ, base_arrangement):
		doc_to_concepts, doc_to_keys, related_concepts = self.get_doc_to_key_concepts(top_n)

		concept_to_score = self.get_concept_to_global_score(related_concepts, doc_to_keys)
		related_concepts = self.get_base_arrangement(related_concepts, concept_to_score, base_arrangement)
		s = SequenceGenerator(self.kg, related_concepts, concept_to_score)
		linear_weighted_sequence = s.get_linear_weighted_sequence()
		docs_sequence =  s.arrange_docs(linear_weighted_sequence, doc_to_keys)
		return docs_sequence, doc_to_keys



