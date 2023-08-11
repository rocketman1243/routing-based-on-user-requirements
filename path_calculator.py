import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt
from filterset import Filterset
from geopy import distance
import os
import random

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

# Utility method for checking path existence that does not explode if source or dest are removed due to 
# insufficiently supported features
def safe_has_path(graph, source, dest) -> bool:
    if source not in graph.nodes or dest not in graph.nodes:
        return False
    else:
        return nx.has_path(graph, source, dest)

def spit_latency(lat0, lon0, lat1, lon1):
    result = distance.distance((lat0, lon0), (lat1, lon1))
    miles = result.miles

    # Method used: https://www.oneneck.com/blog/estimating-wan-latency-requirements/
    # Added 0.5 instead of 2 as this resulted in results closer to this calculator:
    # https://wintelguy.com/wanlat.html 
    latency = (miles * 1.1 + 200) * 2 / 124 + 0.5

    return latency

def fallback_to_ebgp(we_fallback_to_ebgp):
    if we_fallback_to_ebgp:
        print("No path is found, but the PRO does specify to fallback to EBGP, so the request will now be fulfilled by EBGP!")
    else:
        print("No path is found, and the PRO specifies that the request should NOT be forwarded to EBGP. Thus, it ends here. Bye!")

def calculate_paths(nio_path: str, pro, print_all = "no_pls"):

    verbose = print_all == "verbose"
    if verbose:
        print("checking pro from", pro.as_source, "to", pro.as_destination)
    
    we_fallback_to_ebgp = pro.fallback_to_ebgp_if_no_path_found == "true"

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

    #############################################################################################################
    ######## STRICT PHASE #######################################################################################
    #############################################################################################################

    
    if verbose:
        print("\n### STRICT PHASE ###\n")

    filterset = Filterset(pro)

    # Drop nodes that do not comply with strict requirements
    G_strict_phase = filterset.apply_strict_filters(G, pro, nio_objects)

    if G_strict_phase is None:
        if verbose:
            print("No path that adheres to the strict requirements can be found!")

        fallback_to_ebgp(we_fallback_to_ebgp)
        exit(0)
    else:
        if verbose:
            print("At least one path that adheres to strict security requirements", filterset.strict_security_requirements, "and privacy requirements", filterset.strict_privacy_requirements, "exists! Continuing with the best-effort phase!")


    #############################################################################################################
    ######## BEST EFFORT PHASE ##################################################################################
    #############################################################################################################

    if verbose:
        print("\n### BEST EFFORT PHASE ###\n")

    result = filterset.calculate_biggest_satisfiable_subset(G_strict_phase, pro, nio_objects)

    G_best_effort_phase = result[0]
    satisfied_privacy_requirements = result[1]
    satisfied_security_requirements = result[2]


    if len(satisfied_privacy_requirements) + len(satisfied_security_requirements) > 0:
        if verbose:
            print(f"We could satisfy the privacy requirements {satisfied_privacy_requirements} and the security requirements {satisfied_security_requirements}!")
    else:
        if verbose:
            print("No extra best-effort requirements could be satisfied.")
        
    if verbose:
        print("Now, on to the optimization phase!")

    #######################################################################
    ######## Optimization phase ###########################################
    #######################################################################

    if verbose:
        print("\n### OPTIMIZATION PHASE ###\n")

    G_after_filter = copy.deepcopy(G_best_effort_phase)

    # Find all available link-disjoint paths
    all_disjoint_paths = nx.edge_disjoint_paths(G_after_filter, pro.as_source, pro.as_destination)

    # Score them based on the chosen metric & pass on to the multipath pruning phase
    scored_paths = []


    if pro.path_optimization == "minimize_total_latency":
        for path in all_disjoint_paths:
            scored_paths.append([[path], calculate_total_latency(G_after_filter, path)])
    else: # optimization strategy is minimize nr of hops or none, in which case we also minimize hops

        for path in all_disjoint_paths:
            scored_paths.append([path, len(path) - 1])

    # sort scored_paths list by score
    scored_paths.sort(key = lambda x: x[1])

    if verbose:
        print("Here are all possible link-disjoint paths, scored based on the selected optimization strategy (which was", pro.path_optimization + "): ")
    for path in scored_paths:
        if verbose:
            print(path)


    #######################################################################
    ######## Multipath stage ##############################################
    #######################################################################

    if verbose:
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
        fallback_to_ebgp(we_fallback_to_ebgp)
    else:
<<<<<<< HEAD
        if verbose:
            if pro.path_optimization == "minimize_total_latency":
                print("\n The multipath phase selected the", len(multipath_selection), "paths that minimize total latency. Here are the paths, along with their total latency!") 
            else:
                print("\n The multipath phase selected the", len(multipath_selection), "paths that minimize total hopcount. Here are the paths, along with their total hopcount!") 
=======
        if pro.path_optimization == "minimize_total_latency":
            if verbose:
                print("\n The multipath phase selected the", len(multipath_selection), "paths that are most optimal, as determined by your optimization strategy. Here are the paths, along with their total latency!") 
        else:
            if verbose:
                print("\nThe multipath phase selected the", len(multipath_selection), "paths that are most optimal, as determined by your optimization strategy. Here are the paths, along with their total hopcount!") 
>>>>>>> 4116d107e1a6ce15eced16b44f88c21a3568c011
        for path in multipath_selection:
                print(path)


