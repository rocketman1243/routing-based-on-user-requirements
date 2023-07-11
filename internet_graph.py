import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features
from geopy import distance
from copy import deepcopy


G = nx.Graph()


# LINKS

links_filename = "asn_data/as-links.txt"
links_file = open(links_filename)
edges = []
# edge_info = {}

for line in links_file:
    splitted = line.split("|")
    node0 = splitted[0]
    node1 = splitted[1]
    edges.append([node0, node1])

G.add_edges_from(edges)
# nx.set_edge_attributes(G, edge_info)




# Note: Nodes are added based on edges in connected graph
# TODO: Insert extra information from additinal sources into node_info
node_info = {}






nx.set_node_attributes(G, node_info)


################### GENERATE FEATURE DISTRIBUTION & ADD TO GRAPH #################

# After edges are inserted from connected dataset, we generate features based on this
privacy_features_distribution = generate_features(30, G.nodes)
security_features_distribution = generate_features(30, G.nodes)

for node in G.nodes:
    node_info[node]["privacy_features"] = privacy_features_distribution[node]
    node_info[node]["security_features"] = security_features_distribution[node]

nx.set_node_attributes(G, node_info)









############### ANALYSIS & VERIFICATION #################






print("#conn_comp:", nx.number_connected_components(G))

n = list(G.nodes)
path = nx.shortest_path(G, n[0], n[50138])

print(path)







# ONLY use this method on-demand, as it's pretty slow...
# So use it when optimizing paths
    # lat0 = G.nodes[node0]["lat"]
    # lon0 = G.nodes[node0]["lon"]
    # lat1 = G.nodes[node1]["lat"]
    # lon1 = G.nodes[node1]["lon"]
def spit_latency(lat0, lon0, lat1, lon1):
    result = distance.distance((lat0, lon0), (lat1, lon1))
    miles = result.miles

    # Method used: https://www.oneneck.com/blog/estimating-wan-latency-requirements/
    # Added 0.5 instead of 2 as this resulted in results closer to this calculator:
    # https://wintelguy.com/wanlat.html 
    latency = (miles * 1.1 + 200) * 2 / 124 + 0.5

    return latency