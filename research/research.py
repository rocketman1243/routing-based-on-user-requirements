import networkx as nx
import copy
import sys

# filename = sys.argv[1]

G = nx.read_graphml("manhatten.graphml")
# G = nx.Graph()
# with open(filename, "r") as file:
#     for line in file:
#         items = line.split(",")
#         G.add_edge(items[0], items[1])

total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)

# print("#connected components", len(list(nx.connected_components(G))))
# print(filename)
# print(len(G.nodes), "-", filename)
print("#nodes:", len(G.nodes))
print("#edges in G:", len(G.edges))
print("average degree:", average)



