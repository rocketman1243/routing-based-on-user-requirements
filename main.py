import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt
from filterset import Filterset

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

# Build graph
G = nx.Graph()
G.add_nodes_from(as_numbers)
G.add_edges_from(edges)

nx.draw(G)
# plt.show()

# Generate PRO objects
pro_objects = []

for i in range(1, 11):
    filename = f"pro_files/pro_{i}.json"
    pro_file = open(filename)
    pro_content = pro_file.read()
    pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
    pro_objects.append(pro_object)

# Select the first PRO for now

pro = pro_objects[2]

#############################################################################################################
######## STRICT PHASE #######################################################################################
#############################################################################################################

filterset = Filterset(pro.security.strict, pro.privacy.strict, pro.geolocation.exclude)

for as_number in as_numbers:
    print(as_number, filterset.as_has_to_be_removed(nio_objects[as_number], 0))




