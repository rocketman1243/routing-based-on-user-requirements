import networkx as nx
import random


def sortNeighboursOnDescendingDegree(G, neighbours):
    neighboursWithBERIntersectionScore = []
    for n in neighbours:
        degree = nx.degree(G, n)
        neighboursWithBERIntersectionScore.append([n, degree])

    neighboursSortedOnDescendingScore = sorted(
        neighboursWithBERIntersectionScore, key=lambda x: x[1], reverse=True
    )
    sortedNeighbours = list(el[0] for el in neighboursSortedOnDescendingScore)
    return sortedNeighbours


def findRandomPath(G, length):
    path = []
    path.append(random.choice(list(G.nodes)))
    for i in range(length):
        currentNode = path[-1]
        neighbours = list(G.neighbors(currentNode))
        sortedNeighbours = sortNeighboursOnDescendingDegree(G, neighbours)

        for neighbour in sortedNeighbours:
            if neighbour not in path:
                path.append(neighbour)
                break

    return path


def generate_path_with_minimum_length(G, length):
    path = []
    # correctLengthAndShortestPath = False
    # while not correctLengthAndShortestPath:
    #     path = findRandomPath(G, length - 1)
    #     shortestPath = nx.shortest_path(G, path[0], path[-1])
    #     if len(path) == length and len(shortestPath) == length:
    #         correctLengthAndShortestPath = True
    pathLengths = nx.shortest_path_length(G)

    return path


# G = nx.random_internet_as_graph(100)
# print(generate_internet_path(G, 4))
