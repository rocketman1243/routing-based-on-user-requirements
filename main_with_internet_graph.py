import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt
from filterset import Filterset
from geopy import distance
import os
import random

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

# Read in PRO objects
pro_objects = []

for _, _, filenames in os.walk("pro_files/"):
    for filename in filenames:
        with open("pro_files/" + filename) as pro_file:
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
pro = pro_objects[7]
print("checking pro from", pro.as_source, "to", pro.as_destination)












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

# Drop nodes that do not comply with strict requirements
G_strict_phase = filterset.apply_strict_filters(G, pro, nio_objects)

if G_strict_phase is None:
    print("No path that adheres to the strict requirements can be found! Exiting...")
    exit(0)
else:
    print("At least one path that adheres to strict security requirements", filterset.strict_security_requirements, "and privacy requirements", filterset.strict_privacy_requirements, "exists! Continuing with the best-effort phase! \n")


#############################################################################################################
######## BEST EFFORT PHASE ##################################################################################
#############################################################################################################

print("\n### BEST EFFORT PHASE ###\n")

result = filterset.calculate_biggest_satisfiable_subset(G_strict_phase, pro, nio_objects)

G_best_effort_phase = result[0]
satisfied_privacy_requirements = result[1]
satisfied_security_requirements = result[2]


if len(satisfied_privacy_requirements) + len(satisfied_security_requirements) > 0:
    print(f"We could satisfy the privacy requirements {satisfied_privacy_requirements} and the security requirements {satisfied_security_requirements}!")
    
print("Now, on to the optimization phase!")

#######################################################################
######## Optimization phase ###########################################
#######################################################################

print("\n### OPTIMIZATION PHASE ###\n")

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

        lat0 = nio_objects[node0].lat
        lon0 = nio_objects[node0].lon
        lat1 = nio_objects[node1].lat
        lon1 = nio_objects[node1].lon

        latency = spit_latency(lat0, lon0, lat1, lon1)
        total += latency

    return total

if pro.path_optimization == "minimize_total_latency":
    for path in all_disjoint_paths:
        scored_paths.append([[path], calculate_total_latency(G_after_filter, path)])
else: # optimization strategy is minimize nr of hops or none, in which case we also minimize hops

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
    print("There were only", len(scored_paths), "link-disjoint paths available that comply with the requirements. The minimum was", min_nr_of_paths, ", so the request cannot be satisfied :'(")
else:
    if pro.path_optimization == "minimize_total_latency":
        print("\n The multipath phase selected the", len(multipath_selection), "paths that are most optimal, as determined by your optimization strategy. Here are the paths, along with their total latency!") 
    else:
        print("\nThe multipath phase selected the", len(multipath_selection), "paths that are most optimal, as determined by your optimization strategy. Here are the paths, along with their total hopcount!") 
    for path in multipath_selection:
        print(path)




