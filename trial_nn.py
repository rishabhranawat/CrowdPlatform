from sklearn.neighbors import NearestNeighbors
import numpy as np

precomputed_vectors_file = open("/home/ec2-user/collective_store_one/researchModels/models/precomputed.txt", "r")
nodes_file  = open("/home/ec2-user/collective_store_one/CrowdPlatform/seeds_generator/kg_nodes.txt", "r")
nodes = []
vectors = []
for node in nodes_file.readlines():
    nodes.append(node.replace("\n", ""))

for vec in precomputed_vectors_file.readlines():
    v = vec.strip().split(" ")
    a = [float(i) for i in v]
    vectors.append(a)

arr = np.array(vectors)
nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(arr)
print(arr)
