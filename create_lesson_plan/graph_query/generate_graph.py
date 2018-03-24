import networkx as nx
kg = nx.DiGraph()

# Subject and Course nodes
kg.add_node("Computer Science", NodeType = "SubjectNode")
kg.add_node("Introduction to Algorithms", NodeType = "CourseNode")

# Topic 1 -- Sorting
kg.add_node("Sorting", NodeType = "TopicNode")
kg.add_node("Insertion Sort, Bubble Sort", NodeType = "ConceptNode")
kg.add_node("Merge Sort, Quick Sort", NodeType = "ConceptNode")
kg.add_node("Radix Sort, Counting Sort", NodeType = "ConceptNode")

kg.add_edges_from([("Computer Science", "Introduction to Algorithms"),
                  ("Introduction to Algorithms", "Sorting"),
                  ("Sorting", "Insertion Sort, Bubble Sort"),
                  ("Sorting", "Merge Sort, Quick Sort"),
                  ("Sorting", "Radix Sort, Counting Sort")])


# Topic 2 -- Complexity
kg.add_node("Algorithmic Complexity", NodeType = "TopicNode")
kg.add_node("Big Oh Notation", NodeType ="ConceptNode")
kg.add_node("Analysis of Algorithms", NodeType ="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Algorithmic Complexity"),
                  ("Algorithmic Complexity", "Big Oh Notation"),
                  ("Algorithmic Complexity","Analysis of Algorithms")])


# Topic 3 -- Graph Theory
kg.add_node("Graph Theory", NodeType = "TopicNode")
kg.add_node("Representations of graphs", NodeType = "ConceptNode")
kg.add_node("Breadth-first search BFS", NodeType = "ConceptNode")
kg.add_node("Depth-first search DFS", NodeType="ConceptNode")
kg.add_node("Topological Sort", NodeType="ConceptNode")
kg.add_node("Strongly Connected Components", NodeType = "ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Graph Theory"),
                  ("Graph Theory", "Representations of graphs"), 
                  ("Graph Theory", "Breadth-first search BFS"),
                  ("Graph Theory", "Depth-first search DFS"),
                  ("Graph Theory", "Topological Sort"),
                  ("Graph Theory", "Strongly Connected Components"),
                  ("Breadth-first search BFS", "Depth-first search DFS"),
                  ("Depth-first search DFS", "Breadth-first search BFS")])


# Topic 4 -- Divide-and-Conquer
kg.add_node("Divide and Conquer", NodeType="TopicNode")
kg.add_node("Maximum subarray", NodeType="ConceptNode")
kg.add_node("Strassen's matrix multiplication", NodeType="ConceptNode")
kg.add_node("Substitution method solving recurrences", NodeType="ConceptNode")
kg.add_node("Recursion-tree method solving recurrences", NodeType="ConceptNode")
kg.add_node("Master method solving recurrences", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Divide and Conquer"),
                  ("Divide and Conquer", "Maximum subarray"),
                  ("Divide and Conquer", "Strassen's matrix multiplication"),
                  ("Divide and Conquer", "Substitution method solving recurrences"),
                   ("Divide and Conquer", "Recursion-tree method solving recurrences"),
                   ("Divide and Conquer", "Master method solving recurrences")])


# Topic 5 -- Probablistic Analaysis and Randomized Algorithms
kg.add_node("Probablistic Analysis and Randomized Algorithms", NodeType="TopicNode")
kg.add_node("Hiring problem", NodeType="ConceptNode")
kg.add_node("Randomized algorithms", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Probablistic Analysis and Randomized Algorithms"),
                   ("Probablistic Analysis and Randomized Algorithms", "Hiring problem"),
                   ("Probablistic Analysis and Randomized Algorithms", "Randomized algorithms")
                  ])

# Topic 6 -- Heapsort
kg.add_node("Heapsort", NodeType="TopicNode")
kg.add_node("Heaps", NodeType="ConceptNode")
kg.add_node("Maintaining heap property", NodeType="ConceptNode")
kg.add_node("Heapsort algorithm", NodeType="ConceptNode")
kg.add_node("Priority queues", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Heapsort"),
                   ("Heapsort", "Heaps"),
                  ("Heapsort", "Maintaining heap property"),
                  ("Heapsort", "Heapsort algorithm"),
                  ("Heapsort", "Priority queues")])

kg.add_edge("Sorting", "Heapsort")

# Topic 7 -- Medians and Order Statistics
kg.add_node("Medians and Order Statistics")
kg.add_node("Minimum and Maximum")

kg.add_edges_from([("Introduction to Algorithms", "Medians and Order Statistics"),
                  ("Medians and Order Statistics", "Minimum and Maximum")])


# Topic 8 -- Dynamic Programming
kg.add_node("Dynamic Programming", NodeType="TopicNode")
kg.add_node("Rod cutting", NodeType="ConceptNode")
kg.add_node("Elements of dynamic programming", NodeType="ConceptNode")
kg.add_node("Longest common subsequence", NodeType="ConceptNode")
kg.add_node("Optimal binary search trees", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Dynamic Programming"),
                  ("Dynamic Programming", "Rod cutting"),
                  ("Dynamic Programming", "Elements of dynamic programming"),
                  ("Dynamic Programming", "Longest common subsequence"),
                  ("Dynamic Programming", "Optimal binary search trees")])


# Topic 9 -- Greedy Algorithms
kg.add_node("Greedy Algorithms", NodeType="TopicNode")
kg.add_node("Activity selection problem", NodeType="ConceptNode")
kg.add_node("Huffman codes", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Greedy Algorithms"),
                   ("Greedy Algorithms", "Activity selection problem"),
                   ("Greedy Algorithms", "Huffman codes")])

# Topic 10 -- Minimum Spanning Trees
kg.add_node("Minimum Spanning Trees", NodeType="TopicNode")
kg.add_node("Growing a minimum spanning tree", NodeType="ConceptNode")
kg.add_node("Kruskal and Prim algorithms", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Minimum Spanning Trees"),
                  ("Minimum Spanning Trees", "Growing a minimum spanning tree"),
                  ("Minimum Spanning Trees", "Kruskal and Prim algorithms")
                  ])

# Topic 11 - Single Source Shortest Paths
kg.add_node("Single source shortest paths", NodeType="TopicNode")
kg.add_node("Bellman-Ford algorithm", NodeType="ConceptNode")
kg.add_node("single source shortest path in directed acyclic graphs", NodeType="ConceptNode")
kg.add_node("Dijkstra's algorithm", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Single source shortest paths"),
                  ("Single source shortest paths", "Bellman-Ford algorithm"),
                  ("Single source shortest paths", "single source shortest path in directed acyclic graphs"),
                  ("Single source shortest paths", "Dijkstra's algorithm")
                  ])


# Topic 12 -- All pairs shortest paths
kg.add_node("All pairs shortest paths", NodeType="TopicNode")
kg.add_node("Shortest paths and matrix multiplication", NodeType="ConceptNode")
kg.add_node("The Floyd-Warshall algorithm", NodeType="ConceptNode")
kg.add_node("Johnson's algorithm for sparse graphs", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "All pairs shortest paths"),
                  ("All pairs shortest paths", "Shortest paths and matrix multiplication"),
                  ("All pairs shortest paths","The Floyd-Warshall algorithm"),
                   ("All pairs shortest paths", "Johnson's algorithm for sparse graphs")
                  ])

# Topic 13 -- Maximum Flow
kg.add_node("Maximum Flow", NodeType="TopicNode")
kg.add_node("Flow networks", NodeType="ConceptNode")
kg.add_node("The Ford Fulkerson method", NodeType="ConceptNode")
kg.add_node("Maximum bipartite matching", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Maximum Flow"),
                  ("Maximum Flow", "Flow networks"),
                  ("Maximum Flow", "The Ford Fulkerson method"),
                  ("Maximum Flow", "Maximum bipartite matching")])

# Topic 14 -- Mulithreaded Algorithms
kg.add_node("Multithreaded algorithms", NodeType="TopicNode")
kg.add_node("Basics of dynamic multithreading", NodeType="ConceptNode")
kg.add_node("Multithreaded Matrix Multiplication", NodeType="ConceptNode")
kg.add_node("Multithreaded merge sort", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Multithreaded algorithms"),
                  ("Multithreaded algorithms", "Basics of dynamic multithreading"),
                  ("Multithreaded algorithms", "Multithreaded Matrix Multiplication"),
                  ("Multithreaded algorithms", "Multithreaded merge sort")])


# Topic 15 -- Linear Programming
kg.add_node("Linear Programming", NodeType="TopicNode")
kg.add_node("Formulating problems as linear programs", NodeType="ConceptNode")
kg.add_node("Simplex algorithm", NodeType="ConceptNode")
kg.add_node("Duality", NodeType="ConceptNode")
kg.add_node("Basic feasible solution", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Linear Programming"),
                  ("Linear Programming", "Formulating problems as linear programs"),
                  ("Linear Programming", "Simplex algorithm"),
                  ("Linear Programming", "Duality"),
                  ("Linear Programming", "Basic feasible solution")])

# Cross topic edges
kg.add_edge("Sorting", "Analysis of Algorithms")
kg.add_edge("Sorting", "Topological Sort")


# Operating Systems
kg.add_node("Operating Systems", NodeType="CourseNode")
kg.add_edge("Computer Science", "Operating Systems")

kg.add_node("Processes", NodeType="TopicNode")
kg.add_node("Process Creation", NodeType="ConceptNode")
kg.add_node("Process Termination", NodeType="ConceptNode")
kg.add_node("Process States", NodeType="ConceptNode")
kg.add_node("Implementation of Processes", NodeType="ConceptNode")
kg.add_node("Modeling Multiprogramming", NodeType="ConceptNode")

kg.add_edges_from([("Operating Systems", "Processes"),
    ("Processes", "Process Creation"),
    ("Processes", "Process Termination"), 
    ("Processes","Process States"),
    ("Processes", "Implementation of Processes"),
    ("Processes", "Modeling Multiprogramming")
    ])

kg.add_node("Threads", NodeType="TopicNode")
kg.add_node("Thread usage", NodeType="ConceptNode")
kg.add_node("The Classical Thread Model", NodeType="ConceptNode")
kg.add_node("POSIX Threads", NodeType="ConceptNode")
kg.add_node("Implementing Threads in User Space", NodeType="ConceptNode")
kg.add_node("Implementing Threads in the Kernel", NodeType="ConceptNode")

kg.add_edges_from([("Opearting Systems", "Threads"),
    ("Threads", "Thread usage"),
    ("Threads", "The Classical Thread Model"),
    ("Threads", "POSIX Threads"),
    ("Threads", "Implementing Threads in User Space"),
    ("Threads", "Implementing Threads in the Kernel")
    ])



# Machine Learning
kg.add_node("Machine Learning", NodeType="CourseNode")
kg.add_edge("Computer Science", "Machine Learning")

kg.add_node("Supervised Learning", NodeType="TopicNode")
kg.add_node("Linear Algebra", NodeType="ConceptNode")
kg.add_node("Logistic Regression", NodeType="ConceptNode")
kg.add_node("Perceptron", NodeType="ConceptNode")
kg.add_node("Generative Learning Algorithms", NodeType="ConceptNode")
kg.add_node("Gaussian Discriminant Analysis", NodeType="ConceptNode")
kg.add_node("Naive Bayes", NodeType="ConceptNode")
kg.add_node("Support Vector Machines", NodeType="ConceptNode")
kg.add_node("Vectorization", NodeType="ConceptNode")
        
kg.add_edges_from([("Machine Learning", "Supervised Learning"),
    ("Supervised Learning", "Linear Algebra"),
    ("Supervised Learning", "Logistic Regression"),
    ("Supervised Learning", "Perceptron"),
    ("Supervised Learning", "Genearting Learning Algorithms"),
    ("Supervised Learning", "Gaussian Discriminant Analysis"),
    ("Supervised Learning", "Naive Bayes"),
    ("Supervised Learning", "Support Vector Machines"),
    ("Supervised Learning", "Vectorization")
    ])

kg.add_node("Practial ML", NodeType="TopicNode")
kg.add_node("Bias/variance tradeoff", NodeType="ConceptNode")
kg.add_node("Model selection and feature selection", NodeType="ConceptNode")
kg.add_node("Regularization and Model Selection", NodeType="ConceptNode")
kg.add_node("Online Learning and the Perceptron Algorithm", NodeType="ConceptNode")
kg.add_node("Convex Optimization", NodeType="ConceptNode")

kg.add_edges_from([("Machine Learning", "Practical ML"),
    ("Practical ML", "Bias/variance tradeoff"),
    ("Practical ML", "Model selection and feature selection"),
    ("Practical ML", "Regularization and Model Selection"),
    ("Practical ML", "Online Learning and the Perceptron Algorithm"),
    ("Practical ML", "Convex Optimization")
    ])

kg.add_node("Deep Learning", NodeType="TopicNode")
kg.add_node("Neural Network architecture", NodeType="ConceptNode")
kg.add_node("Forward/Backward propagation", NodeType="ConceptNode")

kg.add_edges_from([("Machine Learning", "Deep Learning"),
    ("Deep Learning", "Neural Network architecture"),
    ("Deep Learning", "Forward/Backward propagation"),
    ("Deep Learning", "Optimization")
    ])

kg.add_node("Unsupervised Learning", NodeType="TopicNode")
kg.add_node("K-means clustering", NodeType="ConceptNode")
kg.add_node("Mixture of Gaussians", NodeType="ConceptNode")
kg.add_node("Expecation Maximization", NodeType="ConceptNode")
kg.add_node("Factor Analysis", NodeType="ConceptNode")
kg.add_node("PCA (Principal components analysis)", NodeType="ConceptNode")
kg.add_node("ICA (Indpeendent components analysis", NodeType="ConceptNode")

kg.add_edges_from([("Machine Learning", "Unsupervised Learning"),
    ("Unsupervised Learning", "K-means clustering"),
    ("Unsupervised Learning", "Expectation Maximization"),
    ("Unsupervised Learning", "Mixture of Gaussians"),
    ("Unsupervised Learning", "Factor Analysis"),
    ("Unsupervised Learning", "PCA (Principal components analysis)"),
    ("Unsupervised Learning", "ICA (Independent components analysis)")
    ])


kg.add_node("Reinforcement Learning", NodeType="TopicNode")
kg.add_node("Markov Decision Processes", NodeType="ConceptNode")
kg.add_node("Value iteration and policy iteration", NodeType="ConceptNode")
kg.add_node("Linear quadratic regulation", NodeType="ConceptNode")
kg.add_node("Q-learning", NodeType="ConceptNode")
kg.add_node("Value function approximation", NodeType="ConceptNode")
kg.add_node("Policy search", NodeType="ConceptNode")
kg.add_node("Adversarial Machine Learning", NodeType="ConceptNode")

kg.add_edges_from([("Machine Learning", "Reinforcement Learning"),
    ("Reinforcement Learning", "Markov Decision Processes"),
    ("Reinforcement Learning", "Bellman equations"),
    ("Reinforcment Learning", "Value iteration and policy iteration"),
    ("Reinforcement Learning", "Q-learning"),
    ("Reinforcement Learning", "Value function approximation"),
    ("Reinforcement Learning", "Policy search"), 
    ("Reinforcement Learning", "Adversarial Machine Learning")
    ])

nx.write_gpickle(kg, "graphs/weighted_knowledge_graph.gpickle")
