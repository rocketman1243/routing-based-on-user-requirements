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
This script gets all the links from as-links.txt and converts it into a connected graph
The nodes in this graph form the basis for my internet model
For that to work, I need to gather the country and approximate lat/lon to run the filters on it
This is done from the info in node_attributes.csv, where I combined the info from all kinds of sources into a AS_NUMBER,COUNTRY,LAT,LON csv


"""

number_of_features_in_distribution = 30
min_nr_of_features = 1
output_path = "full_scale_setup/data/nio_files"

dry_run = False



def spit_latency(lat0, lon0, lat1, lon1):
    result = distance.distance((lat0, lon0), (lat1, lon1))
    miles = result.miles

    # Method used: https://www.oneneck.com/blog/estimating-wan-latency-requirements/
    # Added 0.5 instead of 2 as this resulted in results closer to this calculator:
    # https://wintelguy.com/wanlat.html
    latency = round((miles * 1.1 + 200) * 2 / 124 + 0.5, 2)

    return latency



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

G = nx.Graph()


# LINKS

links_file = open("full_scale_setup/data/as-links.txt")
edges = []

for line in links_file:
    splitted = line.split("|")
    node0 = splitted[0]
    node1 = splitted[1]
    edges.append([node0, node1])

G.add_edges_from(edges)

# Note: Nodes are added based on edges in connected graph
node_info = {}

node_info_file = open( "full_scale_setup/data/node_attributes.csv", "r")
for line in node_info_file:
    items = line.split(",")

    asn = items[0]
    country = items[1]

    node_info[asn] = {
        "geolocation": [ country ]
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
features = generate_features(number_of_features_in_distribution, min_nr_of_features, ordered_asns)

with open("./full_scale_setup/data/as_numbers.txt", "w") as file:
    for asn in ordered_asns:
        file.write(asn + "\n")


feature_info = {}
for node in G.nodes:
    feature_info[node] = {}
    feature_info[node]["features"] = features[node]

nx.set_node_attributes(G, feature_info)

print("#nodes in G: ", len(G.nodes))


total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)
print(average, " average degree")
print("#connected components", len(list(nx.connected_components(G))))

#################### SPIT OUT NIO FILES ###########################################

nodes_copy = deepcopy(list(G.nodes))
# bad_nodes = []
print(" hello ", len(nodes_copy))
for asn in nodes_copy:
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
        "geolocation": node["geolocation"],
        "connections": edges_local,
        "latency": latencies,
        "features": node["features"],
    }

    if not dry_run:
        filename = f"{output_path}/nio_" + asn + ".json"
        with open(filename, "w") as file:
            output = json.dumps(nio, indent=2)
            file.write(output)

# print("# bad nodes:", len(bad_nodes))
print("#connected components", len(list(nx.connected_components(G))))
print("#nodes in G:", len(list(G.nodes)))