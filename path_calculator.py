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

def fulfills_strict_requirements(S, F, user_exclude_geolocation, as_geolocations):
    if set(S).issubset(set(F)):
        if len(set(user_exclude_geolocation).intersection(set(as_geolocations))) == 0:
            return True
    return False



def MP(G, pro):

    tic = time.time()

    start = pro.as_source
    end = pro.as_destination

    if not fulfills_strict_requirements(pro.requirements.strict, G.nodes[start]["features"], pro.geolocation.exclude, G.nodes[start]["geolocation"]) or not fulfills_strict_requirements(pro.requirements.strict, G.nodes[end]["features"], pro.geolocation.exclude, G.nodes[end]["geolocation"]):
        # print("strict too strict")
        return 0, 0

    # Tweaking values
    tree_start_depth = 1
    max_tree_depth = 7
    buffer_depth = 0

    neighbour_limit = 5

    # neigh_depth_limit = length of prefix and postfix, aka how far do you stray from the path?
    # detour length can be at most 2 * neigh_depth_limit + 1
    neighbour_depth_limit = 1

    # detour limit = 0 means don't limit just add
    nr_detours_limit = 0
    
    path, ber, improvement, tree_time, detour_time, augment_time = filter_graph(G, pro, tree_start_depth, max_tree_depth, buffer_depth, neighbour_depth_limit, neighbour_limit, nr_detours_limit)

    # print(path)
    # print(ber)
    # print(improvement)

    toc = time.time()
    runtime = toc - tic
    # print("runtime: ", toc - tic)

    return improvement, runtime, tree_time, detour_time, augment_time


    # augment_path_to_biggest_subset(G, pro, path)

    # smartDFS(G, pro, maxDepth)















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

    # print(AllResults)

    # TODO: Optimization part






























def filter_graph(G, pro, startDepth, maxDepth, bufferDepth, neighbour_depth_limit, neighbour_limit, nr_detours_limit):

    tic = time.time()

    complying_nodes = []
    for n in list(G.nodes):
        if fulfills_strict_requirements(pro.requirements.strict, G.nodes[n]["features"], pro.geolocation.exclude, G.nodes[n]["geolocation"]):
            complying_nodes.append(n)

    subgraph = G.subgraph(complying_nodes)

    if nx.has_path(G, pro.as_source, pro.as_destination):
        path = nx.shortest_path(subgraph, pro.as_source, pro.as_destination)
        toc = time.time() - tic

        a, b, c, detour_time, augment_time = augment_path_to_biggest_subset(subgraph, pro, path, neighbour_depth_limit, neighbour_limit, nr_detours_limit)
        return a, b, c, toc, detour_time, augment_time
    else:
        print("strict was too strict (or depth too low)")
        toc = time.time() - tic
        return [], {}, 0, toc, 0, 0
        






























# TODO: Make this supa fast!

def augment_path_to_biggest_subset(G, pro, path, neighbour_depth_limit, neighbour_limit, nr_detours_limit):
    tic = time.time()

    if len(path) < 3:
        # print("path too short to optimize")
        return path 

    # print(path)

    ber = set(pro.requirements.best_effort)

    if(len(ber) == 0):
        # print("no BER so no improvement possible")
        return path, {}, 0, time.time() - tic

    # Store original path and ber for comparison at the end
    # original_path = copy.deepcopy(path)
    before_ber = copy.deepcopy(ber)
    for i in path:
        before_ber = before_ber.intersection(G.nodes[i]["features"])

    # distance = nr of hops between anchor points of detour to path
    # distance 2 means detour around 1 node
    # distance 3 means detour around 2 nodes, etc.
    distances = [2, 3, 4]
    for distance in distances:
        for i in range(len(path) - distance):
            if i + distance + 1 <= len(path):
                a = path[i]
                b = path[i + distance]

                detours, detours_time = find_detours(G, a, b, pro, path, neighbour_depth_limit, neighbour_limit, nr_detours_limit)
                # print(a, b)
                # print("#detours", len(detours))
                # print(detours)
                
                clean_ber = copy.deepcopy(ber)
                for c in path[:i+1] + path[i+distance:]:
                    clean_ber = clean_ber.intersection(G.nodes[c]["features"])

                current_ber = copy.deepcopy(ber)
                for c in path:
                    current_ber = current_ber.intersection(G.nodes[c]["features"])


                if len(clean_ber) <= len(current_ber):
                    # Nothing to improve here, skip this detour
                    continue

                ber_to_beat = copy.deepcopy(current_ber)

                replace_path_segment_with_detour = False
                replacement_detour = []

                for detour in detours:

                    potential_ber = copy.deepcopy(clean_ber)
                    for j in detour:
                        potential_ber = potential_ber.intersection(G.nodes[j]["features"])

                    if len(potential_ber) > len(ber_to_beat):
                        replace_path_segment_with_detour = True
                        replacement_detour = detour
                        ber_to_beat = copy.deepcopy(potential_ber)

                # Replace bad node with detour
                if replace_path_segment_with_detour:
                    potential_path = path[:i+1] + replacement_detour + path[i+distance:]

                    # Ensure no silly mistakes were made
                    if nx.is_simple_path(G, potential_path):
                        path = potential_path





    after_ber = copy.deepcopy(ber)
    for i in path:
        after_ber = after_ber.intersection(G.nodes[i]["features"])

    # if before_ber != after_ber:
    #     print("ber before:", before_ber)
    #     print("path before:", original_path)
    #     print("ber after optimization:", after_ber)
    #     print("path after: ", path)
    # else:
    #     print("----")

    toc = time.time() - tic
    return path, after_ber, len(after_ber) - len(before_ber), detours_time, toc



def limit_neighbours(G, pro, na, nb, neighbour_limit):
    if len(na) > neighbour_limit:
        sorted_na = sorted(list(na), key = lambda x: len(set(G.nodes[x]["features"]).intersection(set(pro.requirements.best_effort))), reverse=True)
        na = set(sorted_na[:neighbour_limit])
    if len(nb) > neighbour_limit:
        sorted_nb = sorted(list(nb), key = lambda x: len(set(G.nodes[x]["features"]).intersection(set(pro.requirements.best_effort))), reverse=True)
        nb = set(sorted_nb[:neighbour_limit])

    return na, nb


def score_detour(G, pro, detour):
    ber = set(pro.requirements.best_effort)
    for n in detour:
        ber = ber.intersection(set(G.nodes[n]["features"]))

    return len(ber)


def add_detour(detours, scores, nr_detours_limit, detour, G, pro):
    if nr_detours_limit == 0:
        detours.append(detour)
        return detours, scores

    if len(detours) < nr_detours_limit:
        detours.append(detour)

    # new_score = score_detour(G, pro, detour)
    # if len(scores) < nr_detours_limit:
    #     detours.append(detour)
    #     scores.append(new_score)
    # else:
    #     for i, score in enumerate(scores):
    #         if new_score > score:
    #             detours[i] = detour
    #             scores[i] = score


    # print("new detour:", detour, new_score, detours, scores)
    return detours, scores


# Find all node sequences that we can use to replace node z from a to b
def find_detours(G, x, y, pro, path, levels, neighbour_limit, nr_detours_limit):

    tic = time.time()

    detours = []
    scores = []

    na = set(nx.neighbors(G, x))
    nb = set(nx.neighbors(G, y))

    # print("na, nb before limit", na, nb)
    na, nb = limit_neighbours(G, pro, na, nb, neighbour_limit)
    # print("na, nb after limit", na, nb)

    # first level
    shared_neighbours = na.intersection(nb).difference(set(path))
    for i in shared_neighbours:
        detours, scores = add_detour(detours, scores, nr_detours_limit, [i], G, pro)

    # second level and onwards
    for aa in na:
        for bb in nb:
            if aa != bb and aa not in path and bb not in path:
                toplevel_prefix = [aa]
                toplevel_postfix = [bb]

                naa = set(nx.neighbors(G, aa))
                nbb = set(nx.neighbors(G, bb))

                reachables = naa.intersection(nbb).difference(set(path))

                for r in reachables:
                    detour = toplevel_prefix + [r] + toplevel_postfix
                    detours, scores = add_detour(detours, scores, nr_detours_limit, detour, G, pro)

                    
                # this is symmetric: If the prefix and postfix are connected, they form a 2-node detour
                if bb in naa:
                    detour = [aa, bb]
                    detours, scores = add_detour(detours, scores, nr_detours_limit, detour, G, pro)
                    
                # print("to third level")
                detours, scores = find_detours_one_level(G, pro, aa, bb, toplevel_prefix, toplevel_postfix, path, 1, levels, neighbour_limit, detours, scores, nr_detours_limit)

    toc = time.time() - tic
    return detours, toc

# TODO: 11, 12, 13, not used for detours. FIX!

def find_detours_one_level(G, pro, aa, bb, toplevel_prefix, toplevel_postfix, path, currentLevel, maxLevel, neighbour_limit, detours, scores, nr_detours_limit):

    currentLevel += 1
    if currentLevel > maxLevel:
        return detours, scores

    # print("in third level")

    naa = set(nx.neighbors(G, aa))
    nbb = set(nx.neighbors(G, bb))

    # nth level
    for aaa in naa:
        for bbb in nbb:
            if aaa != bbb and aaa not in path + toplevel_prefix and bbb not in path + toplevel_postfix:
                prefix = toplevel_prefix + [aaa]
                postfix = [bbb] + toplevel_postfix

                if len(set(prefix).intersection(set(postfix))) != 0:
                    # print("prefix and postfix overlap: ", prefix, postfix)
                    continue


                naaa = set(nx.neighbors(G, aaa))
                nbbb = set(nx.neighbors(G, bbb))


                reachables = naaa.intersection(nbbb).difference(set(path)).difference(set(prefix)).difference(set(postfix))

                # print("in third level: ", aaa, bbb, naaa, nbbb, prefix, postfix, reachables)


                for r in reachables:
                    detour = prefix + [r] + postfix
                    detours, scores = add_detour(detours, scores, nr_detours_limit, detour, G, pro)
                    
                # this is symmetric: If the prefix and postfix are connected, they form a 4-node detour
                if bbb in naaa:
                    detour = prefix + postfix
                    detours, scores = add_detour(detours, scores, nr_detours_limit, detour, G, pro)

                detours, scores = find_detours_one_level(G, pro, aaa, bbb, prefix, postfix, path, currentLevel, maxLevel, neighbour_limit, detours, scores, nr_detours_limit)
    
    return detours, scores






        



