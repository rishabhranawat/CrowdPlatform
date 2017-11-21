import networkx as nx

kg = nx.DiGraph()

kg.add_node("Computer Science", NodeType = "SubjectNode")

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

kg.add_node("Practial ML", NodeType="TopicNode")
kg.add_node("Bias/variance tradeoff", NodeType="ConceptNode")
kg.add_node("Model selection and feature selection", NodeType="ConceptNode")
kg.add_node("Regularization and Model Selection", NodeType="ConceptNode")
kg.add_node("Online Learning and the Perceptron Algorithm", NodeType="ConceptNode")
kg.add_node("Convex Optimization", NodeType="ConceptNode")

kg.add_node("Deep Learning", NodeType="TopicNode")
kg.add_node("NN architecture", NodeType="ConceptNode")
kg.add_node("Forward/Backward propagation", NodeType="ConceptNode")

kg.add_node("Unsupervised Learning", NodeType="TopicNode")
kg.add_node("Clustering. K-means.", NodeType="ConceptNode")
kg.add_node("EM. Mixture of Gaussians", NodeType="ConceptNode")
kg.add_node("Factor Analysis", NodeType="ConceptNode")
kg.add_node("PCA (Principal components analysis)", NodeType="ConceptNode")
kg.add_node("ICA (Indpeendent components analysis", NodeType="ConceptNode")

kg.add_node("Reinforcement Learning", NodeType="TopicNode")
kg.add_node("MDPs. Bellman equations", NodeType="ConceptNode")
kg.add_node("Value iteration and policy iteration", NodeType="ConceptNode")
kg.add_node("Linear quadratic regulation", NodeType="ConceptNode")
kg.add_node("Q-learning. Value function approximation", NodeType="ConceptNode")
kg.add_node("Policy search. Reinforce. POMPDPs", NodeType="ConceptNode")
kg.add_node("Adversarial Machine Learning", NodeType="ConceptNode")

nx.write_gpickle(kg, "ml_graph.gpickle")
