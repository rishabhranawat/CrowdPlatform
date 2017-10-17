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


kg.add_node("Probablistic Analysis and Randomized Algorithms", NodeType="TopicNode")
kg.add_node("Hiring problem", NodeType="ConceptNode")
kg.add_node("Randomized algorithms", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Probablistic Analysis and Randomized Algorithms"),
                   ("Probablistic Analysis and Randomized Algorithms", "Hiring problem"),
                   ("Probablistic Analysis and Randomized Algorithms", "Randomized algorithms")
                  ])

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

kg.add_node("Medians and Order Statistics")
kg.add_node("Minimum and Maximum")

kg.add_edges_from([("Introduction to Algorithms", "Medians and Order Statistics"),
                  ("Medians and Order Statistics", "Minimum and Maximum")])


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


kg.add_node("Greedy Algorithms", NodeType="TopicNode")
kg.add_node("Activity selection problem", NodeType="ConceptNode")
kg.add_node("Huffman codes", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Greedy Algorithms"),
                   ("Greedy Algorithms", "Activity selection problem"),
                   ("Greedy Algorithms", "Huffman codes")])

kg.add_node("Minimum Spanning Trees", NodeType="TopicNode")
kg.add_node("Growing a minimum spanning tree", NodeType="ConceptNode")
kg.add_node("Kruskal and Prim algorithms", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Minimum Spanning Trees"),
                  ("Minimum Spanning Trees", "Growing a minimum spanning tree"),
                  ("Minimum Spanning Trees", "Kruskal and Prim algorithms")
                  ])


kg.add_node("Single source shortest paths", NodeType="TopicNode")
kg.add_node("Bellman-Ford algorithm", NodeType="ConceptNode")
kg.add_node("single source shortest path in directed acyclic graphs", NodeType="ConceptNode")
kg.add_node("Dijkstra's algorithm", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Single source shortest paths"),
                  ("Single source shortest paths", "Bellman-Ford algorithm"),
                  ("Single source shortest paths", "single source shortest path in directed acyclic graphs"),
                  ("Single source shortest paths", "Dijkstra's algorithm")
                  ])



kg.add_node("All pairs shortest paths", NodeType="TopicNode")
kg.add_node("Shortest paths and matrix multiplication", NodeType="ConceptNode")
kg.add_node("The Floyd-Warshall algorithm", NodeType="ConceptNode")
kg.add_node("Johnson's algorithm for sparse graphs", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "All pairs shortest paths"),
                  ("All pairs shortest paths", "Shortest paths and matrix multiplication"),
                  ("All pairs shortest paths","The Floyd-Warshall algorithm"),
                   ("All pairs shortest paths", "Johnson's algorithm for sparse graphs")
                  ])

kg.add_node("Maximum Flow", NodeType="TopicNode")
kg.add_node("Flow networks", NodeType="ConceptNode")
kg.add_node("The Ford Fulkerson method", NodeType="ConceptNode")
kg.add_node("Maximum bipartite matching", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Maximum Flow"),
                  ("Maximum Flow", "Flow networks"),
                  ("Maximum Flow", "The Ford Fulkerson method"),
                  ("Maximum Flow", "Maximum bipartite matching")])

kg.add_node("Multithreaded algorithms", NodeType="TopicNode")
kg.add_node("Basics of dynamic multithreading", NodeType="ConceptNode")
kg.add_node("Multithreaded Matrix Multiplication", NodeType="ConceptNode")
kg.add_node("Multithreaded merge sort", NodeType="ConceptNode")

kg.add_edges_from([("Introduction to Algorithms", "Multithreaded algorithms"),
                  ("Multithreaded algorithms", "Basics of dynamic multithreading"),
                  ("Multithreaded algorithms", "Multithreaded Matrix Multiplication"),
                  ("Multithreaded algorithms", "Multithreaded merge sort")])



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




nx.write_gpickle(kg,"graphs/algorithms.gpickle")