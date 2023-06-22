import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt

# Generate NIO objects
nio_objects = {}
as_numbers = []
edges = []

for i in range(1, 21):
    filename = f"nio_files/nio_{i}.json"
    nio_file = open(filename)
    nio_content = nio_file.read()
    nio_object = json.loads(nio_content, object_hook=lambda nio_content: SimpleNamespace(**nio_content))
    nio_objects[nio_object.as_number] = nio_object

    # Gather graph information
    as_numbers.append(nio_object.as_number)
    latencies = nio_object.latency

    for index, outgoing_edge in enumerate(nio_object.connections):
        edge_data = {
            "latency": latencies[index]
        }
        edge_entry = [nio_object.as_number, outgoing_edge, edge_data]
        edges.append(edge_entry)

print(nio_objects)

# Build graph
G = nx.Graph()
G.add_nodes_from(as_numbers)
G.add_edges_from(edges)

nx.draw(G)
plt.show()

# Generate PRO objects
pro_objects = []

for i in range(1, 11):
    filename = f"pro_files/pro_{i}.json"
    pro_file = open(filename)
    pro_content = pro_file.read()
    pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
    pro_objects.append(pro_object)

class Filterset():
    def __init__(self, security_requirements, privacy_requirements, geolocations_to_exclude):
        this.security_requirements = security_requirements
        this.privacy_requirements = privacy_requirements
        this.geolocations_to_exclude = geolocations_to_exclude

    def this_as_has_to_be_removed(nio_object) -> bool:
        drop: bool = False

        # check security: The required security requirements have to be a subset of the security
        # requirements of the AS to have this AS handle our path. If this is NOT the case, we
        # drop this AS from our graph. Same for privacy...
        if not(set(this.security_requirements).issubset(set(nio_object.security))):
            drop = True
        if not(set(this.privacy_requirements).issubset(set(nio_object.privacy))):
            drop = True

        # Check whether the geolocation(s) of this AS fall in the list of geolocations that we
        # want to EXCLUDE. If so, we drop this AS
        for geolocation in nio_object.geolocation:
            if geolocation in this.geolocations_to_exclude:
                drop = True
                break





