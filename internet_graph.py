import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
from generate_features_distribution import generate_features
from geopy import distance
from copy import deepcopy
import os


""" 
CONTENTS
This script gets all the links from as-links.txt and converts it into a connected graph
The nodes in this graph form the basis for my internet model
For that to work, I need to gather the country and approximate lat/lon to run the filters on it
This is done from multiple sources: 
- DLC0: asns.json (contains all properly registered ASes)
- DLC1: as_to_country + country_to_latlon (fills in most of the gaps)



"""


G = nx.Graph()


# LINKS

links_filename = "additional_data/as-links.txt"
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
node_info = {}

for _, _, files in os.walk("./asn_data"):
    for file in files:
        filename = "asn_data/" + file
        f = open(filename, "r")
        for line in f:
            items = line.split(",")
            asn = items[0]
            country = items[1]
            lat = items[2]
            lon = items[3]

            node_info[asn] = {
                "country": country,
                "lat": lat,
                "lon": lon
            }

nx.set_node_attributes(G, node_info)


################### GENERATE FEATURE DISTRIBUTION & ADD TO GRAPH #################

# After edges are inserted from connected dataset, we generate features based on this
privacy_features_distribution = generate_features(30, G.nodes)
security_features_distribution = generate_features(30, G.nodes)

# TODO: Uncomment this and fix issue later
# for node in G.nodes:
#     node_info[node]["privacy_features"] = privacy_features_distribution[node]
#     node_info[node]["security_features"] = security_features_distribution[node]

# nx.set_node_attributes(G, node_info)









############### ANALYSIS & VERIFICATION #################






print("#conn_comp:", nx.number_connected_components(G))

n = list(G.nodes)
path = nx.shortest_path(G, n[0], n[50138])

print(path)

incomplete_nodes = []
for asn in G.nodes:
    if asn not in node_info:
        incomplete_nodes.append(asn)
        
file = open("get_incomplete_nodes.py", "w")
file.write(f"def get_nodes():\n\treturn {incomplete_nodes}")
file.close()

print("#nodes without metadata: ", len(incomplete_nodes))




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