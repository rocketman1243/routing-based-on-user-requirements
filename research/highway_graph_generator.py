import networkx as nx
import random
import copy
import matplotlib.pyplot as plt

# TODO
"""
remove og edges
remove duplicate highways
"""

def generateHighwayGraph(m, n, minEdgeLength, maxEdgeLength):
    G = nx.grid_2d_graph(m, n)
    updated = {}
    for node in G.nodes:
        updated[node] = False
    nx.set_node_attributes(G, updated, "updated")

    oldG = copy.deepcopy(G)
    oldEdges = oldG.edges

    newNodeCounter = m * n + 1
    for node in oldG.nodes:
        for n in nx.neighbors(oldG, node):
            if not oldG.nodes[n]["updated"]:
                nrOfNewNodes = random.randint(minEdgeLength, maxEdgeLength)
                newNodes = list(range(newNodeCounter, newNodeCounter + nrOfNewNodes))
                newNodeCounter += nrOfNewNodes + 1
                newEdges = []

                for i in range(len(newNodes) - 1):
                    newEdges.append([newNodes[i], newNodes[i + 1]])

                newEdges.append([node, newNodes[0]])
                newEdges.append([n, newNodes[-1]])
                G.add_edges_from(newEdges)

        oldG.nodes[node]["updated"] = True

    G.remove_edges_from(oldEdges)

    # nx.draw(G)
    # plt.draw()
    # plt.show()

    return G

# G = generateHighwayGraph(5, 10, 2, 5)
