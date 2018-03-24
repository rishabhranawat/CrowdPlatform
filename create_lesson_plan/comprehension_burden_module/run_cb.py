import pickle
from comprehension_burden import CB

def aggregate_random_algos(each_arr):
	tots = 0
	pop = []
	for k, v in each_arr.items():
		if("random" in k): 
			tots += v
			pop.append(k)
	if(len(pop) == 0): return each_arr
	each_arr["random"] = tots/len(pop)
	for each in pop:
		each_arr.pop(each)
	return each_arr

def aggregate_random_arrangements(arrangement):
	randoms = []
	pop = []

	# get the random arrangemnt dicts
	for k, v in arrangement.items(): 
		if("random" in k): 
			pop.append(k)
			randoms.append(v)
	if(len(randoms) == 0): return arrangement
	# aggregate them into 1
	random_aggregate = {}
	for r in randoms:
		for k, v in r.items():
			if(k in random_aggregate): random_aggregate[k] += v
			else: random_aggregate[k] = v

	# normalize
	for each_k, v in random_aggregate.items():
			random_aggregate[each_k] = v/len(randoms)
	
	# pop
	for each in pop:
		arrangement.pop(each)

	# add
	arrangement["random"] = random_aggregate
	return arrangement




lps = pickle.load(open("lpobjs.p", "rb"))
lps = {"user_study_graph.txt":lps["user_study_graph_theory_engage.txt"]}

algos = ["linearWeighted", "linear"]
arrangements = ["alphabetical"]

final = {}
for k, v in lps.items():
	print(k)
	c = CB(v)
	arrangement_scores = {}
	for each_arrangement in arrangements:
		each_arr = {}
		for each_algo in algos:
			each_arr[each_algo] = c.get_cb(2, each_algo, each_arrangement)

		normalizer = each_arr["linearWeighted"]
		for key in each_arr.keys():
			each_arr[key] = each_arr[key]/normalizer
		arrangement_scores[each_arrangement] = aggregate_random_algos(each_arr)

	res = (aggregate_random_arrangements(arrangement_scores))
	final[k] = res

arrangements = arrangements[:1]
arrangements.append("random")
for each in arrangements:
	for k, v in final.items():
		print(k)
		if(each in v):
			scores = v[each]
			for algo, sco in scores.items():
				print(algo, sco)
			print("\n")
	print("\n")
	print("\n")




