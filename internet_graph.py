import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace
import random, math

nodes = []
edges = []

asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename)

for line in asn_file:
    asn_object = json.loads(line)
    node = int(asn_object["asn"])
    nodes.append(node)


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

print(len(G.nodes))
print(len(G.edges))


def generate_distribution(max_number_of_features: int, nr_of_ases: int) -> list[int]:
    items_per_step = math.ceil(nr_of_ases / max_number_of_features)

    distribution = []
    counter = 0
    current_number_of_elements = items_per_step
    for i in range(nr_of_ases):
        distribution.append(current_number_of_elements)
        counter += 1

        if counter >= items_per_step:
            counter = 0
            current_number_of_elements -= 1






def generate_features(max_number_of_features: int, as_numbers: list[int]) -> list[int]:
    features = range(1, 31)
    mapping = []

    for index, ass in enumerate(as_numbers):
        sample = random.sample(features, )