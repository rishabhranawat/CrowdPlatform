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


def generateSubOptimalBeamSequence(lp):

	cbCalculator = CB(lp)

	urlToContent = lp.content
	numberOfDocs = lp.number_of_docs
	allDocs = urlToContent.keys()

	docToConcepts, docToKeys, relatedConcepts = cbCalculator.get_doc_to_key_concepts(3)

	beamWidth = 3
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
				nextLevelNodes.add(child)

		nextLevelNodes.sort(key=lambda x: x.cbCalculator, reverse=True)
		nextLevelNodes = nextLevelNodes[0:beamWidth]

	for each in nextLevelNodes:
		print(each.sequenceBurden, each.sequence)




