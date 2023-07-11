import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features
from geopy import distance
from copy import deepcopy

# NODES
nodes = []
node_info = {}

# https://api.asrank.caida.org/dev/docs
asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename)

for line in asn_file:
    asn_object = json.loads(line)
    node = asn_object["asn"]
    nodes.append(node)

    info = {
        "country": asn_object["country"]["iso"],
        "lat": asn_object["latitude"],
        "lon": asn_object["longitude"]
    }
    node_info[node] = info

G = nx.Graph()


# LINKS

links_filename = "asn_data/as-links.txt"
links_file = open(links_filename)
edges = []
edge_info = {}

for line in links_file:
    splitted = line.split("|")
    node0 = splitted[0]
    node1 = splitted[1]
    edges.append([node0, node1])

G.add_edges_from(edges)
# nx.set_edge_attributes(G, edge_info)


counter = 0
connected_nodes = set(list(G.nodes))
metadata_nodes = set(nodes)

nodes_to_gather_info_for_from_other_sources = list(connected_nodes.difference(metadata_nodes))

# Goal: Get:
    # - Country
    # - Lat
    # - Lon


requesturl = "https://api.bgpview.io/asn/"
print("testAS", nodes_to_gather_info_for_from_other_sources[0])









################### GENERATE FEATURE DISTRIBUTION & ADD TO GRAPH #################

# After edges are inserted from connected dataset, we generate features based on this
# privacy_features_distribution = generate_features(30, G.nodes)
# security_features_distribution = generate_features(30, G.nodes)

# for node in G.nodes:
#     node_info[node]["privacy_features"] = privacy_features_distribution[node]
#     node_info[node]["security_features"] = security_features_distribution[node]

# nx.set_node_attributes(G, node_info)









############### ANALYSIS & VERIFICATION #################






print("#conn_comp:", nx.number_connected_components(G))
print("len of nodes and G: ", len(nodes), len(G.nodes))

n = list(G.nodes)
path = nx.shortest_path(G, n[0], n[50138])

# print(path)


nodes.sort()


print(nodes[:20])
print(list(G.nodes)[:20])








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