import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features

nodes = []
edges = []

node_info = {}
edge_info = {}

# https://api.asrank.caida.org/dev/docs
asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename)

for line in asn_file:
    asn_object = json.loads(line)
    node = int(asn_object["asn"])
    nodes.append(node)

    # TODO: Add this to the networkx node object somehow...................
    info = {
        "country": asn_object["country"]["iso"],
        "lat": asn_object["latitude"],
        "lon": asn_object["longitude"]
    }
    node_info[node] = info



links_filename = "asn_data/asnLinks.jsonl"
links_file = open(links_filename)

for line in links_file:
    links_object = json.loads(line)
    node0 = int(links_object["asn0"]["asn"])
    node1 = int(links_object["asn1"]["asn"])
    edges.append([node0, node1])


G = nx.Graph()

G.add_nodes_from(nodes)
G.add_edges_from(edges)




privacy_features_distribution = generate_features(30, G.nodes)
security_features_distribution = generate_features(30, G.nodes)

for node in G.nodes:
    node_info[node]["privacy_features"] = privacy_features_distribution[node]
    node_info[node]["security_features"] = security_features_distribution[node]

nx.set_node_attributes(G, node_info)

print(G.nodes[2]["lat"])