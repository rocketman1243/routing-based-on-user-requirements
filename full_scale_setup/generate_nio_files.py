import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features
from copy import deepcopy
import os
import pprint


""" 
CONTENTS
This script gets all the links from as-links.txt and converts it into a connected graph
The nodes in this graph form the basis for my internet model
For that to work, I need to gather the country and approximate lat/lon to run the filters on it
This is done from the info in node_attributes.csv, where I combined the info from all kinds of sources into a AS_NUMBER,COUNTRY,LAT,LON csv


"""

number_of_features_in_distribution = 30

experiment = "proof_of_concept_experiment"






###################


output_path = experiment + "/nio_files"

G = nx.Graph()


# LINKS

links_file = open("data/as-links.txt")
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
node_info = {}

node_info_file = open( "data/node_attributes.csv", "r")
for line in node_info_file:
    items = line.split(",")

    asn = items[0]
    country = items[1]
    lat = items[2]
    lon = items[3]

    if (lon[-1:] == "\n"):
        lon = lon[:-1]

    node_info[asn] = {
        "geolocation": [ country ],
        "lat": lat,
        "lon": lon
    }

nx.set_node_attributes(G, node_info)

################### GENERATE FEATURE DISTRIBUTION & ADD TO GRAPH #################

degrees = list(nx.degree(G))
degrees.sort(key=lambda x: x[1])
degrees.reverse()

ordered_asns = []
for l in degrees:
    ordered_asns.append(l[0])

# After edges are inserted from connected dataset, we generate features based on this
features = generate_features(number_of_features_in_distribution, ordered_asns)

feature_info = {}
for node in G.nodes:
    feature_info[node] = {}
    feature_info[node]["features"] = features[node]

nx.set_node_attributes(G, feature_info)


total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)
print(average, " average degree")
print("#connected components", len(list(nx.connected_components(G))))

#################### SPIT OUT NIO FILES ###########################################

nodes_copy = deepcopy(list(G.nodes))
for asn in nodes_copy:
    if asn not in node_info:
        G.remove_node(asn)
        continue

    node = G.nodes[asn]
    edges = []
    for e in G.edges(asn):
        edges.append(e[1])

    nio = {
        "as_number": asn,
        "geolocation": node["geolocation"],
        "lat": node["lat"],
        "lon": node["lon"],
        "connections": edges,
        "features": node["features"],
    }

    filename = f"{output_path}/nio_" + asn + ".json"
    with open(filename, "w") as file:
        output = json.dumps(nio, indent=2)
        file.write(output)
