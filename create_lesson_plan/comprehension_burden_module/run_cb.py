import pickle
from comprehension_burden import CB

lps = pickle.load(open("lpobjs.p", "rb"))

for k, v in lps.items():
	c = CB(v)
	print(k)
	print(c.get_cb(2, ["linear", "random", "bfs", "dfs"]))
	print("\n")
