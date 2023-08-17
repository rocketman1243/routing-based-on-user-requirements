import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt
from manrs_filterset import Filterset
from geopy import distance
import os
import random
import time

def calculate_total_latency(graph, nio_objects, path):
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
    latency = round((miles * 1.1 + 200) * 2 / 124 + 0.5, 2)
    
    return latency

def fallback_to_ebgp(we_fallback_to_ebgp, verbose, reason_for_failure):
    if verbose:
        if we_fallback_to_ebgp:
            print("No path is found, but the PRO does specify to fallback to EBGP, so the request will now be fulfilled by EBGP!")
        else:
            print("No path is found, and the PRO specifies that the request should NOT be forwarded to EBGP. Thus, it ends here. Bye!")
    return (0, 0, reason_for_failure, 0, 0, 0, 0)

def calculate_paths(path_to_nio_files: str, pro, print_all = "no_pls"):

    time_start = time.time()

    verbose = print_all == "verbose"
    if verbose:
        print("checking pro from", pro.as_source, "to", pro.as_destination)
    
    we_fallback_to_ebgp = pro.fallback_to_ebgp_if_no_path_found == "true"

    # Generate NIO objects
    nio_objects = {}
    as_numbers = []
    edges = []

    for _,_,files in os.walk(path_to_nio_files):
        for file in files:
            with open(path_to_nio_files + file, "r") as nio_file:
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

    time_after_building_graph = time.time()

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

        return fallback_to_ebgp(we_fallback_to_ebgp, verbose, "strict was too strict")
        exit(0)
    else:
        if verbose:
            print("At least one path that adheres to strict requirements", filterset.strict_requirements, "exists! Continuing with the best-effort phase!")

    time_after_strict_phase = time.time()

    #############################################################################################################
    ######## BEST EFFORT PHASE ##################################################################################
    #############################################################################################################

    if verbose:
        print("\n### BEST EFFORT PHASE ###\n")

    result = filterset.calculate_biggest_satisfiable_subset(G_strict_phase, pro, nio_objects)

    G_best_effort_phase = result[0]
    satisfied_requirements = result[1]

    if verbose:
        if len(satisfied_requirements) > 0:
            print(f"We could satisfy the best-effort requirements {satisfied_requirements}!")
        else:
            print("No extra best-effort requirements could be satisfied.")

        print("Now, on to the optimization phase!")


    time_after_best_effort_phase = time.time()

    #######################################################################
    ######## Optimization phase ###########################################
    #######################################################################

    # TODO: SKIP IF STRATEGY IS NONE

    if verbose:
        print("\n### OPTIMIZATION PHASE ###\n")

    G_after_filter = copy.deepcopy(G_best_effort_phase)

    # Find all available link-disjoint paths
    all_disjoint_paths = nx.edge_disjoint_paths(G_after_filter, pro.as_source, pro.as_destination)

    # Score them based on the chosen metric & pass on to the multipath pruning phase
    scored_paths = []


    if pro.path_optimization == "minimize_total_latency":
        for path in all_disjoint_paths:
            scored_paths.append([path, calculate_total_latency(G_after_filter, nio_objects, path)])
    else: # optimization strategy is minimize nr of hops or none, in which case we also minimize hops
        for path in all_disjoint_paths:
            scored_paths.append([path, len(path) - 1])

    # sort scored_paths list by score
    scored_paths.sort(key = lambda x: x[1])

    # TIE BREAKER: Total degree of path
    # Create dict that maps score to paths. If one score has multiple paths, sort these on descending total degree. 
    # Then reconstruct path ordering from dict
    tied_paths = {} # 
    for path_and_score in scored_paths:
        path = path_and_score[0]
        score = path_and_score[1]
        if score in tied_paths:
            entry = tied_paths[score]
            entry.append(path)
        else:
            entry = [path]

        tied_paths[score] = entry

    tie_is_broken = False
    for score in tied_paths:
        if len(tied_paths[score]) > 1:
            tie_is_broken = True
            path_and_total_degree = []
            # Calculate total degree for each path
            paths = tied_paths[score]
            for path in paths:
                totalDegree = 0
                for asn in path:
                    totalDegree += G.degree[asn]
                path_and_total_degree.append([path, totalDegree])

            # sort and update in dict
            path_and_total_degree.sort(key = lambda x: x[1]) 
            path_and_total_degree.reverse()
            tied_paths[score] = path_and_total_degree

    # Reconstruct path list
    optimized_paths = []
    for key in tied_paths:
        for path in tied_paths[key]:
            optimized_paths.append([path, key])

    if verbose:
        if pro.path_optimization == "none":
            print("Here are all possible link-disjoint paths, scored based on the selected optimization strategy (which was none, so defaulting to minimize_number_of_hops) and the total degree of the path as a tie-breaker if needed:")

            if tie_is_broken:
                print("\n( Path, TotalDegree , Number of Hops)")

        else:
            print("Here are all possible link-disjoint paths, scored based on the selected optimization strategy (which was", pro.path_optimization + "), and the total degree of the path as a tie-breaker if needed: ")

            if tie_is_broken:
                print("\n( Path, TotalDegree , Number of Hops)")

    for path in optimized_paths:
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
        if len(optimized_paths) >= i:
            multipath_selection.extend(optimized_paths[:i])
            break

    if len(multipath_selection) == 0:
        print("There were only", len(optimized_paths), "link-disjoint paths available that comply with the requirements. The minimum was", min_nr_of_paths, ", so the request cannot be satisfied :'(")

        return fallback_to_ebgp(we_fallback_to_ebgp, verbose, "not enough paths for multipath setting")

    else:
        time_after_optimization_phase = time.time()

        round_decimals = 2

        if verbose:
            print("Here are the", len(multipath_selection), "best paths:")
            for path in multipath_selection:
                print(path)

        return (
            len(optimized_paths), 
            len(multipath_selection), 
            "success", 
            round(time_after_building_graph - time_start, round_decimals),
            round(time_after_strict_phase - time_after_building_graph, round_decimals),
            round(time_after_best_effort_phase - time_after_strict_phase, round_decimals),
            round(time_after_optimization_phase - time_after_best_effort_phase, round_decimals),
            round(time_after_optimization_phase - time_start, round_decimals))



