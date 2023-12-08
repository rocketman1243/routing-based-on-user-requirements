import networkx as nx
import json
from copy import deepcopy
import os
import random

prefix = "1_tradeoff_experiment/"

# COMMENT/UNCOMMENT AS NEEDED

# # AS graph
# number_of_nodes = 75000
# G = nx.random_internet_as_graph(number_of_nodes)
# output_path = prefix + "nio_files/as_graph"

# # grid
# number_of_nodes = 100
# G = nx.grid_2d_graph(100, 100)
# output_path = prefix + "nio_files/grid"










maxNrOfFeatures = 100
minNrOfFeatures = 80
dry_run = True


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





# Rename nodes to string to work with the rest of the system
mapping = {}
for n in G.nodes:
    mapping[n] = str(n)
G = nx.relabel_nodes(G, mapping)

node_info = {}

################### GENERATE FEATURE DISTRIBUTION & ADD TO GRAPH #################

def generate_features(number_of_features_per_as: int, min_nr_of_features:int, as_numbers):
    features = list(range(1, number_of_features_per_as + 1))

    mapping = {}

    for as_number in as_numbers:
        mapping[as_number] = random.sample(features, random.randint(0, len(features) - min_nr_of_features) + min_nr_of_features)

    return mapping

features = generate_features(maxNrOfFeatures, minNrOfFeatures, list(G.nodes))

with open(prefix + "/as_numbers.txt", "w") as file:
    for asn in list(G.nodes):
        file.write(asn + "\n")

feature_info = {}
for node in G.nodes:
    feature_info[node] = {}
    feature_info[node]["features"] = features[node]

nx.set_node_attributes(G, feature_info)

# Statistics
total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)
print("average degree:", average)
print("#connected components", len(list(nx.connected_components(G))))
print("#nodes in G:", len(G.nodes))
print("#edges in G:", len(G.edges))

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
