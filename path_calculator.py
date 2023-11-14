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
# - Set up toy network for testing
# - Run MP on toy network, fix (obvious) bugs
# - Run on whole graph

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

    path = nx.shortest_path(G, start, end)
    augment_path_to_biggest_subset(G, pro, path)

def augment_path_to_biggest_subset(G, pro, path):

    if len(path) < 3:
        return path 

    # print(path)    

    ber = set(pro.requirements.best_effort)
    before_ber = copy.deepcopy(ber)
    for i in path:
        before_ber = before_ber.intersection(G.nodes[i]["features"])
    print("ber before optimization:", before_ber)
    print("path before: ", path)

    for i in range(len(path) - 2):
        a = path[i]
        b = path[i + 2]

        find_detours(G, a, b, path, 2)



# Find all node sequences that we can use to replace node z from a to b
def find_detours(G, a, b, path, levels):

    detours = []

    na = set(nx.neighbors(G, a))
    nb = set(nx.neighbors(G, b))

    # first level
    shared_neighbours = na.intersection(nb).difference(set(path))
    for i in shared_neighbours:
        detours.append(i)

    # second level
    for a in na:
        prefix = [a]
        for b in nb:
            postfix = [b]
            if a != b:
                na = set(nx.neighbors(G, a))
                nb = set(nx.neighbors(G, b))
                reachables = na.intersection(nb).difference(set(path))
                for r in reachables:
                    detours.append(prefix + [r] + postfix)
                    
                if b in na:
                    detours.append([a, b])

    print(detours)



        












    # shared_neighbours = set(nx.neighbors(G, a)).intersection(set(nx.neighbors(G, b))).difference(set(path))

    # max_ber_size = len(before_ber)
    # max_j = -1
    # max_ber = before_ber
    # for j in shared_neighbours:
    #     potential_ber = ber.intersection(G.nodes[j]["features"])
    #     if len(potential_ber) > max_ber_size:
    #         # print(potential_ber, ">", before_ber)
    #         max_j = j
    #         max_ber_size = len(potential_ber)

    # current_ber_size = len(ber.intersection(G.nodes[path[i+1]]["features"]))
    # if current_ber_size < max_ber_size:
    #     path[i+1] = max_j

    # after_ber = copy.deepcopy(ber)
    # for i in path:
    #     after_ber = after_ber.intersection(G.nodes[i]["features"])
    # print("ber after optimization:", after_ber)

    # print("path after: ", path)















def filtered_bfs_tree(G, pro, maxDepth):

    # magic number, tweak as you go
    currentDepth = 2

    tree = nx.bfs_tree(G, pro.as_source, True, currentDepth)
    dest_found_in_tree = False
    
    while dest_found_in_tree is False:
        if pro.as_destination in tree.nodes:
            dest_found_in_tree = True
        else:
            currentDepth += 1
            tree = nx.bfs_tree(G, pro.as_source, currentDepth)

    print("found dfs-tree with depth ", currentDepth)
    print("here's increased tree by 2 steps:")
    tree = nx.bfs_tree(G, pro.as_source, currentDepth + 2)
    print(tree.edges)

    subgraph = G.subgraph(tree.nodes)
    # end and start are reversed to search from the end node to reduce search space
    smartDFS(subgraph, pro, pro.as_destination, pro.as_source, currentDepth)
        


def smartDFS(G, pro, start, end, maxDepth):

    # MaxHeap, achieved by multiplying |B| * -1
    AllResults = []

    # Stack to keep memory limited: Stack will grow to at most <maxDepth> size
    Q = []
    Q.append((start, start, [], pro.requirements.best_effort, 0, maxDepth))

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

        if vc == end:
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







