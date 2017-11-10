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
	print(each.text, each.attrib['height'])
