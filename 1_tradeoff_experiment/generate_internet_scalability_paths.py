import networkx as nx
import random

def findRandomPath(G, length):
    path = []
    path.append(random.choice(list(G.nodes)))
    for i in range(length):
        currentNode = path[-1]
        neighbours = list(G.neighbors(currentNode))
        random.shuffle(neighbours)
        for neighbour in neighbours:
            if neighbour not in path:
                path.append(neighbour)
                break

    print("returned path:", path)
    return path


def generate_internet_path(G, length):
    path = []
    correctLengthAndShortestPath = False
    while not correctLengthAndShortestPath:
        path = findRandomPath(G, length - 1)
        shortestPath = nx.shortest_path(G, path[0], path[-1])
        if len(path) == length and len(shortestPath) == length:
            correctLengthAndShortestPath = True
        else:
            print("shortest path:", shortestPath)

    return path


G = nx.random_internet_as_graph(100)
print(generate_internet_path(G, 4))
