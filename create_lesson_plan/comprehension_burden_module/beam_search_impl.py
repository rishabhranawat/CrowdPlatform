import sys
import random
import logging
import json
import time

from os import listdir
from os.path import isfile, join

from comprehension_burden import *


class Node:
	
	def __init__(self, parent, url, sequence):
		self.parent = parent
		self.url = url
		self.sequence = sequence
		self.children = []
		self.sequenceBurden = 0

	def __str__(self):
		return str(self.url) + " children: " + str(len(self.children))

def dfs(root, visited):
	print(root)
	visited.add(root)

	head = root
	toVisit = []

	for each in head.children:
		if(each not in visited):
			toVisit.append(each)
			visited.add(each)
	
	for each in toVisit:
		dfs(each, visited)


'''
Constructs the entire tree with all possibilities
'''
class LessonBeamTree:

	def __init__(self, beamWidth):
		self.beamWidth = beamWidth
		self.nodes = []

	def dfs(self):
		for each in self.nodes:
			dfs(each, set())

	def constructTree(self, docs, roots):
		levelNodes = []
		for root in roots:
			n = Node(None, root, [root])
			levelNodes.append(n)

		rootNodes = [r for r in levelNodes]

		depth = 1
		while(depth < len(docs)):
			nextLevelNodes = []
			for prevNode in levelNodes:
				prevSequence = prevNode.sequence
				for doc in docs:
					newSequence = [x for x in prevSequence]
					newSequence.append(doc)
					newNode = Node(prevNode, doc, newSequence)
					prevNode.children.append(newNode)
					nextLevelNodes.append(newNode)
			depth += 1
			levelNodes = nextLevelNodes

		self.nodes = rootNodes
		return self.nodes


def generateSubOptimalBeamSequence(lp, beamWidth):

	cbCalculator = CB(lp)

	urlToContent = lp.content
	numberOfDocs = lp.number_of_docs
	allDocs = urlToContent.keys()

	docToConcepts, docToKeys, relatedConcepts = cbCalculator.get_doc_to_key_concepts(3)

	if(beamWidth == None):
		beamWidth = len(allDocs)
	lbt = LessonBeamTree(beamWidth)
	roots = lbt.constructTree(allDocs, allDocs[0:beamWidth])

	levelNodes = roots
	while(len(levelNodes) > 0):
		nextLevelNodes = []
		for node in levelNodes:
			prevSequence = node.sequence
			for child in node.children:
				
				if(child.url in prevSequence):
					continue
				newSequence = [x for x in prevSequence]
				newSequence.append(child.url)
				cbCurrentExpansion = cbCalculator.lp_cb(newSequence, docToConcepts, docToKeys)
				child.sequenceBurden = cbCurrentExpansion
				nextLevelNodes.append(child)

		nextLevelNodes.sort(key=lambda x: x.sequenceBurden)
		if(len(nextLevelNodes) == 0):
			break
		levelNodes = nextLevelNodes[0:beamWidth]

	levelNodes.sort(key=lambda x: x.sequenceBurden)
	return levelNodes[0].sequence, levelNodes[0].sequenceBurden

def getAllUrls(docs):
	urls = []
	for each in docs:
		urls.append(each["url"])
	return urls


def groupUrls(docs):
	grouped = {}
	for d in docs:
		typ = d["content_type"]
		if(typ in grouped):
			grouped[typ].append(d["url"])
		else:
			grouped[typ] = [d["url"]]
	return grouped

def getBeamedSequenceAndBurdenCrowdLevel(grouped, beamWidth):
		typ_to_sequence = {}
		total_comprehension_burden = 0

		for k, v in grouped.items():
			lesson_plan = LP(v)
			sequence, cb = generateSubOptimalBeamSequence(lesson_plan, beamWidth)

			typ_to_sequence[k] = sequence
			total_comprehension_burden += cb

		return total_comprehension_burden

def getTDFSWSequenceAndBurden(grouped, algo):
	total_tdfs_weighted_grouped = 0
	for k, v in grouped.items():
		lp = LP(v)
		cb = CB(lp)
		total_tdfs_weighted_grouped += cb.get_cb(2, algo, "random")
	return total_tdfs_weighted_grouped

# traversals = ["bfs", "dfs"]
algoForm = ["beamedMax", "beamed2", "beamed1"]
def run(lps):
	
	fin = ''
	for eachLpData in lps:
		results = {}
		crowdSourced = groupUrls(eachLpData["docs"])
		lpTitle = eachLpData["lesson_title"]

		beamedMax = getBeamedSequenceAndBurdenCrowdLevel(crowdSourced, None)
		results['beamedMax'] = beamedMax/beamedMax
		results['beamed2'] = getBeamedSequenceAndBurdenCrowdLevel(crowdSourced, 2)/beamedMax
		results['beamed1'] =  getBeamedSequenceAndBurdenCrowdLevel(crowdSourced, 1)/beamedMax

		# for trave in traversals:
		# 	cb  = getTDFSWSequenceAndBurden(crowdSourced, trave)
		# 	results[trave] = cb/beamedMax
		
		res = "\\textbf{" + lpTitle.title() + "} "
		for k in algoForm:
			v = results[k]
			res += '& ' + str(round(v, 3)) 
		res += '\\' + '\\' + '\n\\hline \n'
		fin += res
	print(fin)


def crowdDataRunner(arguments):
	latestFiles = ["lesson" + str(count) + ".json" for count in xrange(int(arguments[1]), int(arguments[2]))]
	onlyfiles = ["lps/crowd_sourced_data/"+f for f in listdir("lps/crowd_sourced_data") if f in latestFiles]

	lps = []
	for eachfile in onlyfiles:
		with open(eachfile, 'r') as data:
			json_data = json.load(data)
			lps.append(json_data)
	run(lps)

def runner(arguments):
	lps = []
	with open(arguments[1], 'r') as data:
		json_data = json.load(data)
		lps.append(json_data)
	run(lps)


if __name__ == "__main__":
	arguments = sys.argv[1:]
	if(arguments[0] == 'cd'):
		crowdDataRunner(arguments)
	else:
		runner(arguments)


