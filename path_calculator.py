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
from custom_shortest_path import bidirectional_shortest_path_including_filter, fulfills_strict_requirements

def MP(G, pro, limits):

    tic = time.time()

    start = str(pro.as_source)
    end = str(pro.as_destination)

    if not fulfills_strict_requirements(G, pro, start) or not fulfills_strict_requirements(G, pro, end):
        print("Either start or end did not fulfill the strict requirements, so no path could be found.")
        return 0, 0, 0, 0, 0


    neighbour_depth_limit = limits[0]
    neighbour_limit = limits[1]
    detour_distance_limit = limits[2]

    path, ber, improvement, tree_time, detour_time, augment_time = filter_graph(G, pro, neighbour_depth_limit, neighbour_limit, detour_distance_limit)

    toc = time.time()
    runtime = toc - tic
    return improvement, runtime, tree_time, detour_time, augment_time










def filter_graph(G, pro, neighbour_depth_limit, neighbour_limit, detour_distance_limit):

    tic = time.time()

    if nx.has_path(G, pro.as_source, pro.as_destination):

        path = bidirectional_shortest_path_including_filter(G, pro.as_source, pro.as_destination, pro)
        # print("path:", path)


        toc = time.time() - tic

        a, b, improvement, detour_time, augment_time = augment_path_to_biggest_subset(G, pro, path, neighbour_depth_limit, neighbour_limit, detour_distance_limit)
        return a, b, improvement, toc, detour_time, augment_time
    else:
        print("Graph is not connected and no path could be found")
        toc = time.time() - tic
        return [], {}, 0, toc, 0, 0


# TODO: Make this supa fast!

def augment_path_to_biggest_subset(G, pro, path, neighbour_depth_limit, neighbour_limit, detour_distance_limit):
    tic = time.time()
    detours_time = 0

    if len(path) < 3:
        print("path too short to optimize")
        return path, {}, 0, 0, time.time() - tic

    ber = set(pro.requirements.best_effort)

    if(len(ber) == 0):
        # print("no BER so no improvement possible")
        return path, {}, 0, 0, time.time() - tic

    # Store original path and ber for comparison at the end
    original_path = copy.deepcopy(path)
    before_ber = copy.deepcopy(ber)
    for i in path:
        before_ber = before_ber.intersection(G.nodes[i]["features"])

    skipAmounts = range(2, min(detour_distance_limit, len(original_path)) + 1)
    for skipAmount in skipAmounts:
        for i in range(len(original_path) - skipAmount):
            if original_path[i] in path and original_path[i + skipAmount] in path:
                startIndex = path.index(original_path[i])
                endIndex = path.index(original_path[i + skipAmount])
                detourStart = path[startIndex]
                detourEnd = path[endIndex]
                bottleneck = path[startIndex + 1:endIndex]


                bottleneckFreeBER = copy.deepcopy(ber)
                for c in set(path).difference(set(bottleneck)):
                    bottleneckFreeBER = bottleneckFreeBER.intersection(G.nodes[c]["features"])

                currentPathBER = copy.deepcopy(ber)
                for c in path:
                    currentPathBER = currentPathBER.intersection(G.nodes[c]["features"])


                if len(bottleneckFreeBER) <= len(currentPathBER):
                    # Nothing to improve here, skip this detour
                    continue

                detours, detours_time = find_detours_with_timer(G, detourStart, detourEnd, pro, path, neighbour_limit, neighbour_depth_limit, [], [])
                # print(a, b)
                # print("#detours", len(detours))
                # print("detours:", detours)

                bestBER = copy.deepcopy(currentPathBER)
                bestDetour = []
                updatePath = False

                for detour in detours:
                    potentialBer = copy.deepcopy(bottleneckFreeBER)
                    for j in detour:
                        potentialBer = potentialBer.intersection(G.nodes[j]["features"])

                    if len(potentialBer) > len(bestBER):
                        bestDetour = detour
                        bestBER = copy.deepcopy(potentialBer)
                        updatePath = True

                # Replace bottleneck with detour
                if updatePath:
                    potential_path = path[:startIndex + 1] + bestDetour + path[endIndex:]

                    # Ensure no silly mistakes were made
                    if nx.is_simple_path(G, potential_path):
                        path = potential_path





    after_ber = copy.deepcopy(ber)
    for i in path:
        after_ber = after_ber.intersection(G.nodes[i]["features"])

    # if before_ber != after_ber:
        # print("ber before:", before_ber)
        # print("path before:", original_path)
        # print("ber after optimization:", after_ber)
        # print("path after: ", path)
    # else:
    #     print("----")

    toc = time.time() - tic
    return path, after_ber, len(after_ber) - len(before_ber), detours_time, toc



def limit_neighbours(G, neighbours, PRO, neighbourLimit):

    sortedNeighbours = sorted(neighbours, key = lambda x: len(set(G.nodes[x]["features"]).intersection(set(PRO.requirements.best_effort))), reverse=True)

    if len(neighbours) > neighbourLimit:
        neighbours = sortedNeighbours[:neighbourLimit]
    else:
        neighbours = sortedNeighbours

    # print("sorted neighbours:", neighbours)
    return neighbours

def find_detours_with_timer(G, detourStart, detourEnd, PRO, path, neighbourLimit, depthLimit, prefix, postfix):
    tic = time.time()

    detours = find_detours(G, detourStart, detourEnd, PRO, path, neighbourLimit, depthLimit, prefix, postfix)
    # print("final detours: ", detours)

    toc = time.time() - tic
    return detours, toc

def find_detours(G, detourStart, detourEnd, PRO, path, neighbourLimit, depthLimit, prefix, postfix):
    # print(detourStart, detourEnd)

    if depthLimit == 0:
        return []

    detours = []

    startNeighbours = list(set(nx.neighbors(G, detourStart)).difference(set(path)).difference(set(prefix)).difference(set(postfix)))
    endNeighbours = list(set(nx.neighbors(G, detourEnd)).difference(set(path)).difference(set(prefix)).difference(set(postfix)))

    startNeighbours = limit_neighbours(G, startNeighbours, PRO, neighbourLimit)
    endNeighbours = limit_neighbours(G, endNeighbours, PRO, neighbourLimit)

    shared_neighbours = set(startNeighbours).intersection(set(endNeighbours))

    for i in shared_neighbours:
        if fulfills_strict_requirements(G, PRO, i):
            detours.append(prefix + [i] + postfix)

    # second level and onwards
    for s in startNeighbours:
        for e in endNeighbours:
            if fulfills_strict_requirements(G, PRO, s) and fulfills_strict_requirements(G, PRO, e):
                if s != e and len(set([s, e]).intersection(set(path + prefix + postfix))) == 0:
                        # If the prefix and postfix are connected, they form a 2-node detour
                        if (s, e) in G.edges:
                            detours.append(prefix + [s, e] + postfix)

                        prefix = prefix + [s]
                        postfix = [e] + postfix
                        depthLimit = depthLimit - 1

                        detours = detours + find_detours(G, s, e, PRO, path, neighbourLimit, depthLimit, prefix, postfix)

    return detours


###################################################################



def smartDFS(G, pro, maxDepth):
    tic = time.time()

    # MaxHeap, achieved by multiplying |B| * -1
    # AllResults = []

    # Stack to keep memory limited: Stack will grow to at most <maxDepth> size
    Q = []
    Q.append((pro.as_source, pro.as_destination, [], pro.requirements.best_effort, 0, maxDepth))

    global_best_score = -1
    global_best_path = (0, 0)

    while not len(Q) == 0:
        vc, vp, Pp, Bp, Lp, hopsLeft = Q.pop()

        Pc = copy.deepcopy(Pp)
        Pc.append(vc)

        Bc = copy.deepcopy(Bp)
        Bc = set(Bc).intersection(set(G.nodes[vc]["features"]))

        if len(Bc) < global_best_score:
            # We can never become the best path, so might as well exit
            continue


        # Lc = Lp
        # if vc != vp:
        #     Lc = Lp + G.edges[vp, vc]["latency"]

        if vc == pro.as_destination:
            # heapq.heappush(AllResults, (-1 * len(Bc), Pc, Bc, 0, hopsLeft))

            if len(Bc) > global_best_score:
                global_best_score = len(Bc)
                global_best_path = (len(Bc), len(Pc))


            continue
        if hopsLeft == 0:
            continue

        neighbours_sorted_on_degree = sorted(G.degree(list(nx.neighbors(G, vc))), key=lambda x: x[1], reverse=False)
        neighbours_low_to_high = list(el[0] for el in neighbours_sorted_on_degree)

        for vi in neighbours_low_to_high:
            satisfies_strict_requirements = fulfills_strict_requirements(G, pro, vi)
            if (not (vi in Pc)) and satisfies_strict_requirements and hopsLeft >= 1:
                newHopsLeft = hopsLeft - 1
                Q.append((vi, vc, Pc, Bc, 0, newHopsLeft))

    # print(global_best_path)
    # print(AllResults)

    return time.time() - tic









