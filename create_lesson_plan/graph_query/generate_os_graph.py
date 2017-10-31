import networkx as nx

kg = nx.DiGraph()

# Subject and Course nodes
kg.add_node("Computer Science", NodeType = "SubjectNode")

# Operating Systems
kg.add_node("Operating Systems", NodeType="CourseNode")
kg.add_edge("Computer Science", "Operating Systems")

kg.add_node("Processes", NodeType="TopicNode")

kg.add_node("Demand Paging", NodeType="ConceptNode")
kg.add_node("Concurrent Threads", NodeType="ConceptNode")
kg.add_node("Thrashing and Working Sets", NodeType="ConceptNode")



kg.add_node("Threads", NodeType="TopicNode")
kg.add_node("The Classical Thread Model", NodeType="ConceptNode")
kg.add_node("POSIX Threads", NodeType="ConceptNode")

kg.add_node("Storage Devices", NodeType="ConceptNode")
kg.add_node("File Systems", NodeType="ConceptNode")
kg.add_node("Scheduling", NodeType="ConceptNode")
kg.add_node("Implementing Locks", NodeType="ConceptNode")
kg.add_node("Deadlock", NodeType="ConceptNode")
kg.add_node("Linkers", NodeType="ConceptNode")
kg.add_node("Dynamic Storage Management", NodeType="ConceptNode")
kg.add_node("Virtual Memory", NodeType="ConceptNode")
kg.add_node("Flash Memory", NodeType="ConceptNode")
kg.add_node("Virtual Machines", NodeType="ConceptNode")
kg.add_node("Technology and Operating Systems", NodeType="ConceptNode")


nx.write_gpickle(kg, "os_graph.gpickle")
