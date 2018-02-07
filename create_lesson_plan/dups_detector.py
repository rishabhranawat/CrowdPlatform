class DuplicateDetector:

	def __init__(self):
		self.SHINGLE_SIZE = 20

	def get_shingles(self, f):
		shingles = set()
		buf = f
		for i in range(0, len(buf)-self.SHINGLE_SIZE+1):
			yield buf[i:i+self.SHINGLE_SIZE]

	def jaccard(self, set1, set2):
		x = len(set1.intersection(set2))
		y = len(set1.union(set2))
		return x/float(y)


	def detect(self, content1, content2):
		shingles1 = set(self.get_shingles(content1))
		shingles2 = set(self.get_shingles(content2))

		return self.jaccard(shingles1, shingles2)
