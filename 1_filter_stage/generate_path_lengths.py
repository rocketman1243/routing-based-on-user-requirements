import networkx as nx

prefix = "1_filter_stage/"

# for internet scalability
edges = []
with open(prefix + "as-links.txt", "r") as file:
    for line in file:
        items = line.split("|")
        edges.append([items[0], items[1]])
G = nx.Graph()
G.add_edges_from(edges)

# pathLengths = list(nx.shortest_path_length(G))

# with open(prefix + "internet_path_distances.csv", "w") as file:
#     for i in range(len(pathLengths)):
#         source = pathLengths[i][0]
#         for j in pathLengths[i][1]:
#             dest = j
#             distance = pathLengths[i][1][j]
#             file.write(f"{source},{dest},{distance}\n")

diameter = nx.diameter(G)
with open(prefix + "internet_path_distances.csv", "w") as file:
    file.write(f"diameter: {diameter}\n")
