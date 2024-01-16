from path_calculator import localSearchHeuristic
import os
import json
from types import SimpleNamespace
import networkx as nx

# Read in PRO objects
pro_objects = []

pro_folder = "test_files/pro_files/"
nio_folder = "test_files/nio_files/"
for _, _, filenames in os.walk(pro_folder):
    filenames.sort()
    for filename in filenames:
        with open(pro_folder + filename) as pro_file:
            pro_content = pro_file.read()
            pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
            pro_objects.append(pro_object)

pro = pro_objects[0]

 # Read NIO objects & build graph
nio_objects = []
as_numbers = []
node_info = {}
edges = []
edge_info = {}
for _,_,files in os.walk(nio_folder):
        for file in files:
            with open(nio_folder + file, "r") as nio_file:
                nio_content = nio_file.read()
                nio_object = json.loads(nio_content, object_hook=lambda nio_content: SimpleNamespace(**nio_content))

                as_numbers.append(nio_object.as_number)
                node_info[nio_object.as_number] = {
                    "features": nio_object.features,
                    "filtered": False
                }
                here = nio_object.as_number
                for index, other in enumerate(nio_object.connections):
                    edges.append([here, other])

# Build graph
G = nx.Graph()
G.add_nodes_from(as_numbers)
nx.set_node_attributes(G, node_info)
G.add_edges_from(edges)


newHops, hopDiff, totalBER, improvement, runtime, timeAfterPath = localSearchHeuristic(G, pro, [2, 2])

print(improvement)