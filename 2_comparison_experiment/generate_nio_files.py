import networkx as nx
import json
from copy import deepcopy
import os
import random
from highway_graph_generator import generateHighwayGraph
from generate_features_distribution import generate_linear_features

prefix = "2_comparison_experiment/"



# experiment = "as_graph"
# experiment = "as_graph_ber_5"
# experiment = "as_graph_ber_25"
experiment = "as_graph_ber_500"
# experiment = "city"
# experiment = "flights"
# experiment = "village"


minNrOfFeatures = 400
maxNrOfFeatures = 500

dry_run = False

# COMMENT/UNCOMMENT AS NEEDED

output_path = ""
if "as_graph" in experiment:
    G = nx.random_internet_as_graph(500)
    output_path = prefix + "nio_files/" + experiment

if experiment == "city":
    G = nx.grid_2d_graph(22, 23)
    output_path = prefix + "nio_files/city"

if experiment == "flights":
    G = nx.powerlaw_cluster_graph(500, 6, 0.01)
    output_path = prefix + "nio_files/flights"

if experiment == "village":
    G = generateHighwayGraph(10, 10, 1, 4)
    output_path = prefix + "nio_files/village"


if len(output_path) == 0:
    print("no experiment recognized")
    exit(0)





if dry_run:
    print("DRY RUN")


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
if "linear" in experiment:
    features = generate_linear_features(maxNrOfFeatures, minNrOfFeatures - 1, G.nodes, G)

as_numbers_path = prefix + "as_numbers/" + experiment + "_as_numbers.txt"
with open(as_numbers_path, "w") as file:
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
print(output_path)
print("#nodes in G:", len(G.nodes))
print("#edges in G:", len(G.edges))
print("average degree:", average)
print("#connected components", len(list(nx.connected_components(G))))

#################### SPIT OUT NIO FILES ###########################################

for asn in list(G.nodes):
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
