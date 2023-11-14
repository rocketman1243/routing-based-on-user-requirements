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

# TODO:

- Set up toy network for testing
- Run MP on toy network, fix (obvious) bugs
- Run on whole graph



def MP(G, pro, maxDepth):

    start = pro.as_source
    end = pro.as_destination

    if not fulfills_strict_requirements(pro.requirements.strict, G.nodes[start]["features"], pro.geolocation.exclude, G.nodes[start]["geolocation"]) or not fulfills_strict_requirements(pro.requirements.strict, G.nodes[end]["features"], pro.geolocation.exclude, G.nodes[end]["geolocation"]):
        return None

    # MaxHeap, achieved by multiplying |B| * -1
    AllResults = []

    # Priorityqueue, where pop gives the element with the biggest Bc
    Q = []
    heapq.heappush(Q, (-1 * len(pro.requirements.best_effort), pro.as_source, pro.as_source, [], pro.requirements.best_effort, 0, maxDepth))

    while not len(Q) == 0:
        priority, vc, vp, Pc, Bc, Lc, hopsLeft = heapq.heappop(Q)

        Pc.append(vc)
        Bc = set(Bc).intersection(set(G.nodes[vc]["features"]))
        if vc != vp:
            Lc = Lc + G.edges[vp, vc]["latency"]

        if vc == end:
            heapq.heappush(AllResults, (-1 * len(Bc), Pc, Bc, Lc, hopsLeft))
            continue

        for vi in nx.neighbors(G, vc):
            satisfies_strict_requirements = fulfills_strict_requirements(pro.requirements.strict, G.nodes[vi]["features"], pro.geolocation.exclude, G.nodes[vi]["geolocation"]) 
            if (not (vi in Pc)) and satisfies_strict_requirements and len(Pc) <= 10:
                hopsLeft = hopsLeft - 1
                heapq.heappush(Q, (-1 * len(Bc), vi, vc, Pc, Bc, Lc, hopsLeft))

    print(AllResults)

    # TODO: Optimization part







