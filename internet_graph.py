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
    node = int(asn_object["asn"])
    nodes.append(node)

    info = {
        "country": asn_object["country"]["iso"],
        "lat": asn_object["latitude"],
        "lon": asn_object["longitude"]
    }
    node_info[node] = info

G = nx.Graph()

G.add_nodes_from(nodes)
privacy_features_distribution = generate_features(30, G.nodes)
security_features_distribution = generate_features(30, G.nodes)

for node in G.nodes:
    node_info[node]["privacy_features"] = privacy_features_distribution[node]
    node_info[node]["security_features"] = security_features_distribution[node]

nx.set_node_attributes(G, node_info)


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


nodes_readonly = deepcopy(nodes)
print("before trim: ", len(G.nodes))
for node in nodes_readonly:
    if G.degree(node) == 0:
        G.remove_node(node)
        nodes.remove(node)

print("after trim: ", len(G.nodes))

print("#conn_comp:", nx.number_connected_components(G))

n = list(G.nodes)
path = nx.shortest_path(G, n[0], n[50138])

print(path)


# TODO: Deze nodes zijn wel connected (1 connected component), maar sommige missen metadata.
# Mijn taak wordt nu om die metadata toe te voegen/op te zoeken voor de ASes die het nog niet hebben

# Maar eerst de overheid....









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