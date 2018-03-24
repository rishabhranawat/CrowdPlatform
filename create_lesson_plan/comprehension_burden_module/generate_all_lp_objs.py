from comprehension_burden import LP
import os
import pickle

lps = {}
for root, dirs, files in os.walk("lps/engage/"):  
    for filename in files:
    	print(filename)
        lp = LP("lps/engage/"+filename)
        lps[filename] = lp
        print("done")
pickle.dump(lps, open("lpobjs.p", "wb"))