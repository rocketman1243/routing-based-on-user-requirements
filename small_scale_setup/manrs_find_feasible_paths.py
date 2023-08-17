import os
import random
import copy
import networkx as nx
import json
from types import SimpleNamespace


def generate_valid_pro_data():

    nio_path = "manrs_nio_files/"

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
    features = [
        "filtering",
        "anti_spoofing",
        "coordination",
        "routing_information"
    ] 

    # For geolocation, we keep track of the geolocations and later on ensure that we pick a sample of geolocations that does not occur in our path
    geolocations = set()

    # For reference: We should keep minimum_number_of_paths always at 1, as we can only guarantee one path using this method (for now...)

    for asn in path:
        nio = nio_objects[asn]
        # Filter features
        features_copy = copy.deepcopy(features)
        for feature in features_copy:
            if feature not in nio.features:
                features.remove(feature)

        # Gather geolocation
        geolocations.update(nio.geolocation)

    return (endpoints, features, list(geolocations))
