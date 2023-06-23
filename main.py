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

# Utility method for checking path existence that does not explode if source or dest are removed due to 
# insufficiently supported features
def safe_has_path(graph, source, dest) -> bool:
    # print("hello", graph.nodes, source, dest)
    if source not in graph.nodes or dest not in graph.nodes:
        return False
    else:
        return nx.has_path(graph, source, dest)


# Select the first PRO for now
pro = pro_objects[0]



# TEMPORARY Sanity check
path_exists = safe_has_path(G, pro.as_source, pro.as_destination)

if not(path_exists):
    print("No path exists at all! Exiting...")
    exit(0)


#############################################################################################################
######## STRICT PHASE #######################################################################################
#############################################################################################################

filterset = Filterset(pro)
as_numbers_after_strict_phase = []
G_strict_phase = copy.deepcopy(G)

# Drop nodes that do not comply with strict requirements
for num in as_numbers:
    if filterset.as_has_to_be_removed(nio_objects[num], "strict", "not_verbose"):
        if num in [pro.as_source, pro.as_destination]:
            # No path can be found as the source or destinaton does not comply
            # Exit and cry in a corner
            print("Either source or destination does not comply with the strict reqiurements, so no path can ever be found.\nExiting...")
            exit()
    else:
        as_numbers_after_strict_phase.append(num)

# Try to find path
path_exists = safe_has_path(G_strict_phase, pro.as_source, pro.as_destination)


if not(path_exists):
    print("No path that adheres to the strict requirements can be found! Exiting...")
    exit(0)
else:
    print("Path that adheres to strict privacy requirements", filterset.strict_privacy_requirements, "and security requirements", filterset.strict_security_requirements, "exists:\n", nx.shortest_path(G_strict_phase, pro.as_source, pro.as_destination), "\nContinuing with the best-effort phase!")


#############################################################################################################
######## BEST EFFORT PHASE ##################################################################################
#############################################################################################################

G_best_effort_phase = copy.deepcopy(G_strict_phase)
source_and_destination_comply_with_first_set_of_best_effort = True


# Drop nodes that do not comply with strict AND all best effort requirements
for num in as_numbers_after_strict_phase:
    if filterset.as_has_to_be_removed(nio_objects[num], "best_effort", "not_verbose"):
        G_best_effort_phase.remove_node(num)

# Try to find path
path_exists = safe_has_path(G_best_effort_phase, pro.as_source, pro.as_destination)

if path_exists:
    best_effort_path = nx.shortest_path(G_best_effort_phase, pro.as_source, pro.as_destination)
    print("Found a best-effort path: ", best_effort_path)

while not(path_exists):
    filterset.reduce_best_effort_security_constraints()
    filterset.reduce_best_effort_privacy_constraints()

    # Start with a fresh graph such that we can again remove nodes
    G_best_effort_phase = copy.deepcopy(G_strict_phase)

    # Drop nodes that do not comply with strict AND reduced set of best effort requirements
    for num in as_numbers_after_strict_phase:
        if filterset.as_has_to_be_removed(nio_objects[num], "best_effort", "not_verbose"):
            G_best_effort_phase.remove_node(num)

    print("hi")
    path_exists = safe_has_path(G_best_effort_phase, pro.as_source, pro.as_destination)

best_effort_path = nx.shortest_path(G_best_effort_phase, pro.as_source, pro.as_destination)

print("Best effort shortest path found that adheres to best effort security requirements", filterset.best_effort_security_requirements, "and privacy requirements", filterset.best_effort_privacy_requirements, "found:\n", nx.shortest_path(G_best_effort_phase, pro.as_source, pro.as_destination), "\nContinuing with the optimizaiton phase!")






