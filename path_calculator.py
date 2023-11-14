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
    # path = ['1', '2', '6', '5']
    augment_path_to_biggest_subset(G, pro, path)

def augment_path_to_biggest_subset(G, pro, path):

    if len(path) < 3:
        return path 

    # print(path)    

    ber = set(pro.requirements.best_effort)

    before_ber = copy.deepcopy(ber)

    for i in path:
        before_ber = before_ber.intersection(G.nodes[i]["features"])

    print("path before: ", path)

    for i in range(len(path) - 2):
        a = path[i]
        b = path[i + 2]

        detours = find_detours(G, a, b, path, 2)
        
        clean_ber = copy.deepcopy(ber)
        for c in path[:i+1] + path[i+2:]:
            clean_ber = clean_ber.intersection(G.nodes[c]["features"])
        print("clean ber:", clean_ber)

        best_ber = {}

        # TODO: Fix BER calculation and path replacement

        print(detours)
        replace_detour = False
        replacement_detour = []

        for detour in detours:

            potential_ber = copy.deepcopy(clean_ber)
            max_ber = copy.deepcopy(best_ber)

            for j in detour:
                potential_ber = potential_ber.intersection(G.nodes[j]["features"])

            if len(potential_ber) > len(max_ber):
                print(potential_ber, ">", max_ber)
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
        print("ber after optimization:", after_ber)

        print("path after: ", path)





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
    # a should be connected with a, and
    for aa in na:
        prefix = [aa]
        for bb in nb:
            postfix = [bb]
            if aa != bb and aa not in path and bb not in path:
                naa = set(nx.neighbors(G, aa))
                nbb = set(nx.neighbors(G, bb))
                print(aa, naa, bb, nbb)

                reachables = naa.intersection(nbb).difference(set(path))
                print(reachables)

                for r in reachables:
                    detours.append(prefix + [r] + postfix)
                    
                if bb in na:
                    detours.append([aa, bb])

    return detours



        

























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







