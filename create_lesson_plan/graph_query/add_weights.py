import networkx as nx

kg = nx.read_gpickle("graphs/knowledge_graph.gpickle")

kg["Graph Theory"]["Representations of graphs"]["weight"] = 6
kg["Graph Theory"]["Breadth-first search BFS"]["weight"] = 5
kg["Graph Theory"]["Depth-first search DFS"]["weight"] = 5
kg["Graph Theory"]["Topological Sort"]["weight"] = 4
kg["Graph Theory"]["Strongly Connected Components"]["weight"] = 3

kg["Divide and Conquer"]["Maximum subarray"]["weight"]= 5
kg["Divide and Conquer"]["Strassen's matrix multiplication"]["weight"]= 4
kg["Divide and Conquer"]["Substitution method solving recurrences"]["weight"]= 3
kg["Divide and Conquer"]["Recursion-tree method solving recurrences"]["weight"]= 2
kg["Divide and Conquer"]["Master method solving recurrences"]["weight"]= 1

kg["Dynamic Programming"]["Rod cutting"]["weight"] = 4
kg["Dynamic Programming"]["Elements of dynamic programming"]["weight"] = 3
kg["Dynamic Programming"]["Longest common subsequence"]["weight"] = 4
kg["Dynamic Programming"]["Optimal binary search trees"]["weight"] = 2

kg["Single source shortest paths"]["Bellman-Ford algorithm"]["weight"] = 2
kg["Single source shortest paths"]["single source shortest path in directed acyclic graphs"]["weight"] = 2
kg["Single source shortest paths"]["Dijkstra's algorithm"]["weight"] = 3


kg["Processes"]["Process Creation"]["weight"] = 5
kg["Processes"]["Process Termination"]["weight"] = 4
kg["Processes"]["Process States"]["weight"] = 3
kg["Processes"]["Implementation of Processes"]["weight"] = 2
kg["Processes"]["Modeling Multiprogramming"]["weight"] = 1

kg["Threads"]["Thread usage"]["weight"] = 5
kg["Threads"]["The Classical Thread Model"]["weight"] = 4
kg["Threads"]["POSIX Threads"]["weight"] = 3
kg["Threads"]["Implementing Threads in User Space"]["weight"] = 2
kg["Threads"]["Implementing Threads in the Kernel"]["weight"] = 1

kg["Supervised Learning"]["Linear Algebra"]["weight"] = 8
kg["Supervised Learning"]["Logistic Regression"]["weight"] = 7
kg["Supervised Learning"]["Perceptron"]["weight"] = 6
kg["Supervised Learning"]["Genearting Learning Algorithms"]["weight"] = 4
kg["Supervised Learning"]["Gaussian Discriminant Analysis"]["weight"] = 2
kg["Supervised Learning"]["Naive Bayes"]["weight"] = 4
kg["Supervised Learning"]["Support Vector Machines"]["weight"] = 5
kg["Supervised Learning"]["Vectorization"]["weight"] = 1

kg["Unsupervised Learning"]["K-means clustering"]["weight"] = 6
kg["Unsupervised Learning"]["Expectation Maximization"]["weight"] = 5
kg["Unsupervised Learning"]["Mixture of Gaussians"]["weight"] = 4
kg["Unsupervised Learning"]["Factor Analysis"]["weight"] = 3
kg["Unsupervised Learning"]["PCA (Principal components analysis)"]["weight"]= 2
kg["Unsupervised Learning"]["ICA (Independent components analysis)"]["weight"]= 1

kg["Practical ML"]["Bias/variance tradeoff"]["weight"] = 5
kg["Practical ML"]["Model selection and feature selection"]["weight"] = 4
kg["Practical ML"]["Regularization and Model Selection"]["weight"] = 3
kg["Practical ML"]["Online Learning and the Perceptron Algorithm"]["weight"] = 2
kg["Practical ML"]["Convex Optimization"]["weight"] = 1

nx.write_gpickle(kg, "graphs/weighted_knowledge_graph.gpickle")