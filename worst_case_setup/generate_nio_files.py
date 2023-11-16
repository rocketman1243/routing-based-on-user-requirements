import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features
from copy import deepcopy
import os
import pprint
from geopy import distance
import random

""" 
CONTENTS
This script creates a worst case network and turns it into a collection of NIO files
to be consumed by main.py


"""

number_of_nodes = 30000
number_of_features_in_distribution = 100
output_path = "worst_case_setup/data/nio_files"

dry_run = False



###################

# Cleanup previous files in directory as the number of objects may be less than before, 
# causing dead files from previous runs to still exist

if not dry_run:
    files = os.listdir(output_path)
    for file in files:
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


#######################3

# See https://networkx.org/documentation/stable/reference/generated/networkx.generators.internet_as_graphs.random_internet_as_graph.html#networkx.generators.internet_as_graphs.random_internet_as_graph for the source of this wonderful item
G = nx.random_internet_as_graph(number_of_nodes)

# Statistics
total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)
print(average, " average degree")
print("#connected components", len(list(nx.connected_components(G))))



# Rename nodes to string to work with the rest of the system
mapping = {}
for n in G.nodes:
    mapping[n] = str(n)
G = nx.relabel_nodes(G, mapping)

# Note: Nodes are added based on edges in connected graph
node_info = {}

################### GENERATE FEATURE DISTRIBUTION & ADD TO GRAPH #################

# After edges are inserted from connected dataset, we generate features based on this
features = generate_features(number_of_features_in_distribution, list(G.nodes))

with open("./worst_case_setup/data/as_numbers.txt", "w") as file:
    for asn in list(G.nodes):
        file.write(asn + "\n")

feature_info = {}
for node in G.nodes:
    feature_info[node] = {}
    feature_info[node]["features"] = features[node]

nx.set_node_attributes(G, feature_info)

print("#nodes in G: ", len(G.nodes))

#################### SPIT OUT NIO FILES ###########################################

for asn in list(G.nodes):
    # if asn not in node_info:
    #     bad_nodes.append(asn)
    #     continue

    node = G.nodes[asn]
    edges_local = []
    latencies = []
    for e in G.edges(asn):

        latency = random.randint(2, 100)
        edges_local.append(e[1])
        latencies.append(latency)

    nio = {
        "as_number": asn,
        "geolocation": [],
        "connections": edges_local,
        "latency": latencies,
        "features": node["features"],
    }

    if not dry_run:
        filename = f"{output_path}/nio_" + asn + ".json"
        with open(filename, "w") as file:
            output = json.dumps(nio, indent=2)
            file.write(output)

print("#nodes in G:", len(list(G.nodes)))