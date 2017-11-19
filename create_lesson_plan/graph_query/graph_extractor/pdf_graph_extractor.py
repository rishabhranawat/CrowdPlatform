import pdfquery
pdf =  pdfquery.PDFQuery("/Users/rishabh/Desktop/algorithms_clrs.pdf")
pdf.load(6)

tree = pdf.tree
root = tree.getroot()

allds = []
for each in root.getchildren():
	for p in each.getchildren():
		for d in p.getchildren():
			allds.append(d)

allds.sort(key=lambda x: x.attrib['height'], reverse=True)

for each in allds:
	if(each.text != '' and each.text != None):
		print(each.text, each.attrib['height'])

import numpy as np

X = np.array([[3.1, 10], [3.2, 11], [1.1, 0], [1.2, 1], [2.1, 4], [2.2, 5], [2.3, 6], [2.8, 7], [3.0, 9]])

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
for each in X:
	print(each, kmeans.predict(np.array(each)))
