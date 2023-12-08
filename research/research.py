import networkx as nx
import copy

filename = "research/kingsburg.csv"

G = nx.Graph()
with open(filename, "r") as file:
    for line in file:
        items = line.split(",")
        G.add_edge(items[0], items[1])

counter = 0
for node in copy.deepcopy(G.nodes):
    if nx.degree(G, node) == 1:
        counter += 1

print(counter)

total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)
print("#connected components", len(list(nx.connected_components(G))))
print(filename)
print("#nodes in G:", len(G.nodes))
print("#edges in G:", len(G.edges))
print("average degree:", average)

