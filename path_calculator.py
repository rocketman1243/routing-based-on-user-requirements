import json
from types import SimpleNamespace
import networkx as nx
import copy
import matplotlib.pyplot as plt
from filterset import Filterset
from geopy import distance
import os
import random
import time
import math
import queue
import heapq

# TODO:
# - Set up worst case setup
# - Show that it is indeed worst case setup
# - Go supa fast


def fulfills_strict_requirements(S, F, user_exclude_geolocation, as_geolocations):
    if set(S).issubset(set(F)):
        if len(set(user_exclude_geolocation).intersection(set(as_geolocations))) == 0:
            return True
    return False





def MP(G, pro, maxDepth):

    start = pro.as_source
    end = pro.as_destination

    if not fulfills_strict_requirements(pro.requirements.strict, G.nodes[start]["features"], pro.geolocation.exclude, G.nodes[start]["geolocation"]) or not fulfills_strict_requirements(pro.requirements.strict, G.nodes[end]["features"], pro.geolocation.exclude, G.nodes[end]["geolocation"]):
        print("strict too strict")
        return None

    # path = nx.shortest_path(G, start, end)
    # augment_path_to_biggest_subset(G, pro, path)

    smartDFS(G, pro, maxDepth)















def smartDFS(G, pro, maxDepth):

    # MaxHeap, achieved by multiplying |B| * -1
    AllResults = []

    # Stack to keep memory limited: Stack will grow to at most <maxDepth> size
    Q = []
    Q.append((pro.as_source, pro.as_destination, [], pro.requirements.best_effort, 0, maxDepth))

    while not len(Q) == 0:
        vc, vp, Pp, Bp, Lp, hopsLeft = Q.pop()
        # print(vp, vc, Pp, Bp)

        Pc = copy.deepcopy(Pp)
        Pc.append(vc)

        Bc = copy.deepcopy(Bp)
        Bc = set(Bc).intersection(set(G.nodes[vc]["features"]))
        Lc = Lp
        if vc != vp:
            Lc = Lp + G.edges[vp, vc]["latency"]

        if vc == pro.as_destination:
            heapq.heappush(AllResults, (-1 * len(Bc), Pc, Bc, Lc, hopsLeft))
            continue
        if hopsLeft == 0:
            continue

        neighbours_sorted_on_degree = sorted(G.degree(list(nx.neighbors(G, vc))), key=lambda x: x[1], reverse=False)
        neighbours_low_to_high = list(el[0] for el in neighbours_sorted_on_degree)

        for vi in neighbours_low_to_high:
            satisfies_strict_requirements = fulfills_strict_requirements(pro.requirements.strict, G.nodes[vi]["features"], pro.geolocation.exclude, G.nodes[vi]["geolocation"]) 
            if (not (vi in Pc)) and satisfies_strict_requirements and hopsLeft >= 1:
                newHopsLeft = hopsLeft - 1
                Q.append((vi, vc, Pc, Bc, Lc, newHopsLeft))

    print(AllResults)

    # TODO: Optimization part






























def filtered_bfs_tree(G, pro, maxDepth):

    # magic number, tweak as you go
    currentDepth = 2

    tree = nx.bfs_tree(G, pro.as_source, True, currentDepth)
    dest_found_in_tree = False
    
    while dest_found_in_tree is False and currentDepth < maxDepth:
        if pro.as_destination in tree.nodes:
            dest_found_in_tree = True
        else:
            currentDepth += 1
            tree = nx.bfs_tree(G, pro.as_source, currentDepth)

    tree = nx.bfs_tree(G, pro.as_source, currentDepth + 2)
    reverse_tree = nx.bfs_tree(G, pro.as_destination, currentDepth + 2)
    complying_nodes = []
    for n in list(tree.nodes) + list(reverse_tree.nodes):
        if fulfills_strict_requirements(pro.requirements.strict, G.nodes[n]["features"], pro.geolocation.exclude, G.nodes[n]["geolocation"]):
            complying_nodes.append(n)

    subgraph = G.subgraph(complying_nodes)
    if nx.has_path(subgraph, pro.as_source, pro.as_destination):
        # smartDFS(subgraph, pro, pro.as_source, pro.as_destination, currentDepth)
        path = nx.shortest_path(subgraph, pro.as_source, pro.as_destination)
        # print(path)
        # print(len(G.nodes))
        augment_path_to_biggest_subset(subgraph, pro, path)

    else:
        print("strict was too strict")
        































def augment_path_to_biggest_subset(G, pro, path):

    if len(path) < 3:
        print("path too short to optimize")
        return path 


    ber = set(pro.requirements.best_effort)

    if(len(ber) == 0):
        print("no BER so no improvement possible")
        return

    original_path = copy.deepcopy(path)

    before_ber = copy.deepcopy(ber)

    for i in path:
        before_ber = before_ber.intersection(G.nodes[i]["features"])

    for i in range(len(path) - 2):
        a = path[i]
        b = path[i + 2]

        detours = find_detours(G, a, b, path, 2)
        
        clean_ber = copy.deepcopy(ber)
        for c in path[:i+1] + path[i+2:]:
            clean_ber = clean_ber.intersection(G.nodes[c]["features"])
        if len(clean_ber) == len(before_ber):
            continue
        # print("clean ber:", clean_ber)

        best_ber = {}

        # TODO: Fix BER calculation and path replacement

        # print(detours)
        replace_detour = False
        replacement_detour = []

        for detour in detours:

            potential_ber = copy.deepcopy(clean_ber)
            max_ber = copy.deepcopy(best_ber)

            for j in detour:
                potential_ber = potential_ber.intersection(G.nodes[j]["features"])

            if len(potential_ber) > len(max_ber):
                # print(potential_ber, ">", max_ber)
                max_ber = copy.deepcopy(potential_ber)

            if len(best_ber) < len(max_ber):
                replace_detour = True
                replacement_detour = detour
                best_ber = copy.deepcopy(max_ber)

        if replace_detour:
            # Replace bad node with detour
            path = path[:i+1] + replacement_detour + path[i+2:]





    after_ber = copy.deepcopy(ber)
    for i in path:
        after_ber = after_ber.intersection(G.nodes[i]["features"])

    if before_ber != after_ber:
        print("ber before:", before_ber)
        print("path before:", original_path)
        print("ber after optimization:", after_ber)
        print("path after: ", path)
    else:
        print("while we tried there was no improvement possible over:", before_ber)





# Find all node sequences that we can use to replace node z from a to b
def find_detours(G, x, y, path, levels):

    detours = []

    na = set(nx.neighbors(G, x))
    nb = set(nx.neighbors(G, y))

    # first level
    shared_neighbours = na.intersection(nb).difference(set(path))
    for i in shared_neighbours:
        detours.append([i])

    # second level
    for aa in na:
        prefix = [aa]
        for bb in nb:
            postfix = [bb]
            if aa != bb and aa not in path and bb not in path:
                naa = set(nx.neighbors(G, aa))
                nbb = set(nx.neighbors(G, bb))
                reachables = naa.intersection(nbb).difference(set(path))

                for r in reachables:
                    detours.append(prefix + [r] + postfix)
                    
                if bb in naa:
                    detours.append([aa, bb])

    # third level
    # TODO


    return detours



        



