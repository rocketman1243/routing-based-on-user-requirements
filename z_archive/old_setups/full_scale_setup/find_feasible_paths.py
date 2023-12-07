import os
import random
import copy
import networkx as nx
import json
from types import SimpleNamespace
import random


def perform_random_walk(G, start_node):
    length = random.randint(10, 100)
    path = []
    current_node = start_node
    for i in range(length):
        path.append(current_node)
        current_node = random.choice(list(G.edges(current_node)))[1]
    return path




def generate_valid_pro_data(experiment):

    nio_path = experiment + "/nio_files/"

    # Generate NIO objects
    nio_objects = {}
    as_numbers = []
    edges = []

    for _,_,files in os.walk(nio_path):
        for file in files:
            with open(nio_path + file, "r") as nio_file:
                nio_content = nio_file.read()
                nio_object = json.loads(nio_content, object_hook=lambda nio_content: SimpleNamespace(**nio_content))
                nio_objects[nio_object.as_number] = nio_object

                as_numbers.append(nio_object.as_number)

                for index, outgoing_edge in enumerate(nio_object.connections):
                    # This can be updated later when edge data _is_ needed. For now its empty.
                    edge_data = {
                    }
                    edge_entry = [nio_object.as_number, outgoing_edge, edge_data]
                    edges.append(edge_entry)

    # Build graph
    G = nx.Graph()
    G.add_nodes_from(as_numbers)
    G.add_edges_from(edges)

    # find path
    start_node = random.choice(as_numbers)
    path = perform_random_walk(G, start_node)
    endpoints = [start_node, path[-1]]

    # Gather the requirements that all nodes on this path support
    # We start with everything, and remove what is not supported by any of the nodes on the path
    supported_features = list(range(1, 31))

    # For geolocation, we keep track of the geolocations and later on ensure that we pick a sample of geolocations that does not occur in our path
    geolocations = set()

    # For reference: We should keep minimum_number_of_paths always at 1, as we can only guarantee one path using this method (for now...)

    for asn in path:
        nio = nio_objects[asn]
        # Filter features
        feature_copy = copy.deepcopy(supported_features)
        for feature in feature_copy:
            if feature not in nio.features:
                supported_features.remove(feature)

        # Gather geolocation
        geolocations.add(nio.geolocation[0])

    return (endpoints, supported_features, list(geolocations))
