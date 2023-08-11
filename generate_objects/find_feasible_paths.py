import os
import random
import copy
import networkx as nx
import json
from types import SimpleNamespace


def generate_valid_pro_data():

    nio_path = "../nio_files/"

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
    endpoints = random.sample(as_numbers, 2)
    path = nx.shortest_path(G, endpoints[0], endpoints[1])

    # Gather the requirements that all nodes on this path support
    # We start with everything, and remove what is not supported by any of the nodes on the path
    supported_privacy_features = list(range(1, 31))
    supported_security_features = list(range(1, 31))

    # For geolocation, we keep track of the geolocations and later on ensure that we pick a sample of geolocations that does not occur in our path
    geolocations = set()

    # For reference: We should keep minimum_number_of_paths always at 1, as we can only guarantee one path using this method (for now...)

    for asn in path:
        nio = nio_objects[asn]
        # Filter features
        privacy_copy = copy.deepcopy(supported_privacy_features)
        for feature in privacy_copy:
            if feature not in nio.privacy:
                supported_privacy_features.remove(feature)

        security_copy = copy.deepcopy(supported_security_features)
        for feature in security_copy:
            if feature not in nio.security:
                supported_security_features.remove(feature)

        # Gather geolocation
        geolocations.add(nio.geolocation[0])

    return (endpoints, supported_privacy_features, supported_security_features, list(geolocations))

result = generate_valid_pro()
print(result)