import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features

nodes = []
geolocations = {}

edges = []

# https://api.asrank.caida.org/dev/docs
asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename)

for line in asn_file:
    asn_object = json.loads(line)
    node = int(asn_object["asn"])

    # TODO: Add this to the networkx node object somehow...................
    info = {
        "country": asn_object["country"]["iso"],
        "lat": asn_object["latitude"],
        "lon": asn_object["longitude"]
    }



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

nx.set_node_attributes(G, privacy_features_distribution, "privacy_features")
nx.set_node_attributes(G, security_features_distribution, "security_features")
