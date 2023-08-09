import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt
from filterset import Filterset
from geopy import distance
import os

# Generate NIO objects
nio_objects = {}
as_numbers = []
edges = []

for _,_,files in os.walk("./nio_files"):
    for file in files:
        with open("nio_files/" + file, "r") as nio_file:
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

# # Generate PRO objects
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
    if source not in graph.nodes or dest not in graph.nodes:
        return False
    else:
        return nx.has_path(graph, source, dest)


# Select the first PRO for now
pro = pro_objects[0]



# TEMPORARY Sanity check
path_exists = safe_has_path(G, pro.as_source, pro.as_destination)

if not(path_exists):
    print("No path exists at all, even without filtering! Exiting...")
    exit(0)


#############################################################################################################
######## STRICT PHASE #######################################################################################
#############################################################################################################

print("\n### STRICT PHASE ###\n")

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
    print("At least one path that adheres to strict privacy requirements", filterset.strict_privacy_requirements, "and security requirements", filterset.strict_security_requirements, "exists! Continuing with the best-effort phase! \n")


#############################################################################################################
######## BEST EFFORT PHASE ##################################################################################
#############################################################################################################

print("\n### BEST EFFORT PHASE ###\n")

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

    path_exists = safe_has_path(G_best_effort_phase, pro.as_source, pro.as_destination)


if len(filterset.best_effort_privacy_requirements) + len(filterset.best_effort_security_requirements) == 0:
    print("Unfortunately the best effort requirements could not be satisfied. However, we can still find a path that satisfies the strict requirements. Thus, we now go to the optimization phase!! \n")
else:
    print("At least one best effort path that adheres to best effort security requirements", filterset.best_effort_security_requirements, "and privacy requirements", filterset.best_effort_privacy_requirements, " exists! Continuing with the optimization phase! \n")

#######################################################################
######## Optimization phase ###########################################
#######################################################################

print("\n### OPTIMIZATION PHASE ###\n")

    #  lat0 = G.nodes[node0]["lat"]
    #  lon0 = G.nodes[node0]["lon"]
    #  lat1 = G.nodes[node1]["lat"]
    #  lon1 = G.nodes[node1]["lon"]
    #  latency = spit_latency(lat0, lon0, lat1, lon1)
def spit_latency(lat0, lon0, lat1, lon1):
    result = distance.distance((lat0, lon0), (lat1, lon1))
    miles = result.miles

    

    # Method used: https://www.oneneck.com/blog/estimating-wan-latency-requirements/
    # Added 0.5 instead of 2 as this resulted in results closer to this calculator:
    # https://wintelguy.com/wanlat.html 
    latency = (miles * 1.1 + 200) * 2 / 124 + 0.5

    return latency

G_after_filter = copy.deepcopy(G_best_effort_phase)

# Find all available link-disjoint paths
all_disjoint_paths = nx.edge_disjoint_paths(G_after_filter, pro.as_source, pro.as_destination)

# Score them based on the chosen metric & pass on to the multipath pruning phase
scored_paths = []

def calculate_total_latency(graph, path):
    total = 0
    for i in range(len(path) - 1):
        node0 = path[i]
        node1 = path[i + 1] 

        latency = G_after_filter[path[i]][path[i + 1]]["latency"]

        total += latency

    return total

if pro.path_optimization == "minimize_total_latency":
    for path in all_disjoint_paths:
        scored_paths.append([[path], calculate_total_latency(G_after_filter, path)])
else: # optimization strategy is minimize nr of hops
    for path in all_disjoint_paths:
        scored_paths.append([path, len(path) - 1])

# sort scored_paths list by score
scored_paths.sort(key = lambda x: x[1])

print("Here are all possible link-disjoint paths, scored based on the selected optimization strategy (which was", pro.path_optimization + "): ")
for path in scored_paths:
    print(path)


#######################################################################
######## Multipath stage ##############################################
#######################################################################

print("\n### MULTIPATH PHASE ###\n")

min_nr_of_paths = pro.multipath.minimum_number_of_paths
target_nr_of_paths = pro.multipath.target_amount_of_paths

multipath_selection = []
for i in range(target_nr_of_paths, min_nr_of_paths - 1, -1):
    if len(scored_paths) >= i:
        multipath_selection.extend(scored_paths[:i])
        break

if len(multipath_selection) == 0:
    print("There were only", len(scored_paths), "link-disjoint paths available that comply with the requirements. The minimum was", min_nr_of_paths, ", so the request cannot be satisfied :D")
else:
    if pro.path_optimization == "minimize_total_latency":
        print("\n The multipath phase selected the", len(multipath_selection), "paths that are most optimal, as determined by your optimization strategy. Here are the paths, along with their total latency!") 
    else:
        print("\nThe multipath phase selected the", len(multipath_selection), "paths that are most optimal, as determined by your optimization strategy. Here are the paths, along with their total hopcount!") 
    for path in multipath_selection:
        print(path)




