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
from custom_shortest_path import bidirectionalBFSWithFilter, fulfillsStrictRequirements

def MP(G, pro, limits):

    tic = time.time()

    start = str(pro.as_source)
    end = str(pro.as_destination)

    if not fulfillsStrictRequirements(G, pro, start) or not fulfillsStrictRequirements(G, pro, end):
        print("Either start or end did not fulfill the strict requirements, so no path could be found.")
        return 0, 0, 0

    depthLimit = limits[0]
    neighbourLimit = limits[1]

    timeBeforePath = time.time()
    path = bidirectionalBFSWithFilter(G, pro)
    timeAfterPath = time.time() - timeBeforePath

    if len(path) == 0:
        toc = time.time() - tic
        return [], 0, toc

    newPath, totalBER, improvement = augmentPathToBiggestSubset(G, pro, path, depthLimit, neighbourLimit)

    toc = time.time()
    runtime = toc - tic

    print("heuristic path:", newPath, "heuristic BER:", )

    return len(newPath), len(newPath) - len(path), totalBER, improvement, runtime, timeAfterPath





def augmentPathToBiggestSubset(G, pro, path, depthLimit, neighbourLimit):

    ber = set(pro.requirements.best_effort)

    if(len(ber) == 0):
        # print("no BER so no improvement possible")
        return path, 0, 0

    # Store original path and ber for comparison at the end
    originalPath = copy.deepcopy(path)
    beforeBER = copy.deepcopy(ber)
    for i in path:
        beforeBER = beforeBER.intersection(G.nodes[i]["features"])


    if len(path) < 3:
        print("path too short to optimize")
        return path, len(beforeBER), 0

    detourDistances = range(2, len(originalPath))
    for detourDistance in detourDistances:
        for i in range(len(originalPath) - detourDistance):
            if originalPath[i] in path and originalPath[i + detourDistance] in path:
                startIndex = path.index(originalPath[i])
                endIndex = path.index(originalPath[i + detourDistance])
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

                detours = find_detours(G, detourStart, detourEnd, pro, path, neighbourLimit, depthLimit, [], [])
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





    afterBER = copy.deepcopy(ber)
    for i in path:
        afterBER = afterBER.intersection(G.nodes[i]["features"])

    # if beforeBER != afterBER:
    #     print("ber before:", beforeBER)
    #     print("path before:", originalPath)
    print("ber after optimization:", afterBER)
    #     print("path after: ", path)
    # else:
    #     print("----")

    return path, len(afterBER), len(afterBER) - len(beforeBER)



def limit_neighbours(G, neighbours, PRO, neighbourLimit):

    sortedNeighbours = sorted(neighbours, key = lambda x: len(set(G.nodes[x]["features"]).intersection(set(PRO.requirements.best_effort))), reverse=True)

    if len(neighbours) > neighbourLimit:
        neighbours = sortedNeighbours[:neighbourLimit]
    else:
        neighbours = sortedNeighbours

    # print("sorted neighbours:", neighbours)
    return neighbours


def find_detours(G, detourStart, detourEnd, PRO, path, depthLimit, neighbourLimit, prefix, postfix):
    # print("detour call,", detourStart, detourEnd)

    if depthLimit == 0:
        return []

    detours = []

    startNeighbours = list(set(nx.neighbors(G, detourStart)).difference(set(path)).difference(set(prefix)).difference(set(postfix)))
    endNeighbours = list(set(nx.neighbors(G, detourEnd)).difference(set(path)).difference(set(prefix)).difference(set(postfix)))

    startNeighbours = limit_neighbours(G, startNeighbours, PRO, neighbourLimit)
    endNeighbours = limit_neighbours(G, endNeighbours, PRO, neighbourLimit)

    shared_neighbours = set(startNeighbours).intersection(set(endNeighbours))

    for i in shared_neighbours:
        if fulfillsStrictRequirements(G, PRO, i):
            detours.append(prefix + [i] + postfix)

    # second level and onwards
    for s in startNeighbours:
        for e in endNeighbours:
            if fulfillsStrictRequirements(G, PRO, s) and fulfillsStrictRequirements(G, PRO, e):
                if s != e and len(set([s, e]).intersection(set(path + prefix + postfix))) == 0:
                        # If the prefix and postfix are connected, they form a 2-node detour
                        if (s, e) in G.edges:
                            detours.append(prefix + [s, e] + postfix)

                        prefix = prefix + [s]
                        postfix = [e] + postfix

                        detours = detours + find_detours(G, s, e, PRO, path, neighbourLimit, depthLimit - 1, prefix, postfix)

    return detours


###################################################################



def globalBFS(G, pro, maxDepth):
    tic = time.time()

    # MaxHeap, achieved by multiplying |B| * -1
    # AllResults = []

    # Stack to keep memory limited: Stack will grow to at most <maxDepth> size
    Q = []
    Q.append((pro.as_source, pro.as_destination, [], pro.requirements.best_effort, 0, maxDepth))

    globalBestScoreNrBER = -1
    globalBestPathLength = (0, 0)
    globalBestPath = []
    globalBestBER = {}

    while not len(Q) == 0:
        vc, vp, Pp, Bp, Lp, hopsLeft = Q.pop()

        Pc = copy.deepcopy(Pp)
        Pc.append(vc)

        Bc = copy.deepcopy(Bp)
        Bc = set(Bc).intersection(set(G.nodes[vc]["features"]))

        if len(Bc) < globalBestScoreNrBER:
            # We can never become the best path, so might as well exit
            continue


        # Lc = Lp
        # if vc != vp:
        #     Lc = Lp + G.edges[vp, vc]["latency"]

        if vc == pro.as_destination:
            # heapq.heappush(AllResults, (-1 * len(Bc), Pc, Bc, 0, hopsLeft))

            if len(Bc) > globalBestScoreNrBER:
                globalBestScoreNrBER = len(Bc)
                globalBestPathLength = len(Pc)
                globalBestPath = Pc
                globalBestBER = Bc


            continue
        if hopsLeft == 0:
            continue

        neighbours_sorted_on_degree = sorted(G.degree(list(nx.neighbors(G, vc))), key=lambda x: x[1], reverse=False)
        neighbours_low_to_high = list(el[0] for el in neighbours_sorted_on_degree)

        for vi in neighbours_low_to_high:
            satisfies_strict_requirements = fulfillsStrictRequirements(G, pro, vi)
            if (not (vi in Pc)) and satisfies_strict_requirements and hopsLeft >= 1:
                newHopsLeft = hopsLeft - 1
                Q = [(vi, vc, Pc, Bc, 0, newHopsLeft)] + Q

    print("globalBFS path:", globalBestPath, "BER:", globalBestBER)
    # print(AllResults)

    return globalBestPathLength, globalBestScoreNrBER









