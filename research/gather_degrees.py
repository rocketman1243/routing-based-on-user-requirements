import networkx as nx
import copy
import sys
from scipy import stats
import matplotlib.pyplot as plt
from highway_graph_generator import generateHighwayGraph

nowrite = True

## as graph
# map = "as_graph"
# G = nx.Graph()
# with open("as-links", "r") as file:
#     for line in file:
#         items = line.split("|")
#         G.add_edge(items[0], items[1])
# H = nx.random_internet_as_graph(75388)

## city
map = "city"
# F = nx.read_graphml("manhatten.graphml")
F = nx.read_graphml("old_files/newyork.graphml")
G = F.to_undirected()

H = nx.grid_2d_graph(64, 69)


## flights
# map = "flights"
# G = nx.Graph()
# with open("flights-LARGE.txt", "r") as file:
#     for line in file:
#         items = line.split(" ")
#         G.add_edge(items[0], items[1])
# H = nx.powerlaw_cluster_graph(6827, 6, 0.001)

## village
# map = "village"
# G = nx.Graph()
# with open("village.csv") as file:
#     for line in file:
#         items = line.split(",")
#         G.add_edge(items[0], items[1])
# H = generateHighwayGraph(15, 15, 2, 10)


################################################################################3

total_degree = 0
degrees = []
for node in G.nodes:
    total_degree += nx.degree(G, node)
    degrees.append(nx.degree(G, node))
average = total_degree / len(G.nodes)

if not nowrite:
    with open(f"{map}_dataset_degrees.txt", "w") as file:
        for degree in degrees:
            file.write(f"{degree}\n")

print("#connected components", len(list(nx.connected_components(G))))
print("#nodes:", len(G.nodes))
print("#edges in G:", len(G.edges))
# print("average degree:", average)

comparison_total_degree = 0
comparison_degrees = []
for node in H.nodes:
    comparison_total_degree += nx.degree(H, node)
    comparison_degrees.append(nx.degree(H, node))
comparison_average = comparison_total_degree / len(H.nodes)
print("comparison #nodes:", len(H.nodes))
print("comparison #edges in G:", len(H.edges))
# print("comparison average degree:", average)

if not nowrite:
    with open(f"{map}_generator_degrees.txt", "w") as file:
        for degree in comparison_degrees:
            file.write(f"{degree}\n")


# print(degrees)
# print(comparison_degrees)

# print(stats.ks_2samp(degrees, comparison_degrees, method="asymp"))


# target = 4416

# for i in range(40, 80):
#     for j in range(40, 80):
#         if i * j == target:
#             print(i, j, i * j)
