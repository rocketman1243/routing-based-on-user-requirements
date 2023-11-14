from path_calculator import MP
import os
import json
from types import SimpleNamespace
import networkx as nx

small_scale_proof_of_concept_path = "small_scale_setup/proof_of_concept_experiment"
small_scale_realistic_paths_experiment = "small_scale_setup/realistic_paths_experiment"

full_scale_proof_of_concept_experiment_path = "full_scale_setup/proof_of_concept_experiment"

#######################


initial_results_path = "full_scale_setup/initial_results_experiment"
cost_of_control_experiment_path =  "full_scale_setup/cost_of_control_experiment"
as_path_experiment_path = "full_scale_setup/as_path_experiment"
scalability_experiment_path = "full_scale_setup/scalability_experiment"
optimization_trade_off_experiment = "full_scale_setup/optimization_trade_off_experiment"

test_path = "test_files"

maxDepth = 10


CHOSEN_PATH = test_path


# Read in PRO objects   
pro_objects = []

for _, _, filenames in os.walk(f"{CHOSEN_PATH}/pro_files/"):
    filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for filename in filenames:
        with open(f"{CHOSEN_PATH}/pro_files/" + filename) as pro_file:
            pro_content = pro_file.read()
            pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
            pro_objects.append(pro_object)


# Read NIO objects & build graph
path_to_nio_files = f"{CHOSEN_PATH}/../data/nio_files/" 

# For test: 
path_to_nio_files = "test_files/nio_files/"

nio_objects = []
as_numbers = []
node_info = {}
edges = []
edge_info = {}
for _,_,files in os.walk(path_to_nio_files):
        for file in files:
            with open(path_to_nio_files + file, "r") as nio_file:
                nio_content = nio_file.read()
                nio_object = json.loads(nio_content, object_hook=lambda nio_content: SimpleNamespace(**nio_content))

                if "scalability_experiment" in path_to_nio_files:
                    nio_object.features = []

                as_numbers.append(nio_object.as_number)
                node_info[nio_object.as_number] = {
                    "geolocation": nio_object.geolocation,
                    "features": nio_object.features
                }
                here = nio_object.as_number
                for index, other in enumerate(nio_object.connections):
                    edge_info = {
                        "latency": nio_object.latency[index]
                    }
                    edges.append([here, other, edge_info])

# Build graph
G = nx.Graph()
G.add_nodes_from(as_numbers)
nx.set_node_attributes(G, node_info)
G.add_edges_from(edges)


for i in range(len(pro_objects)):
    print("pro", i + 1, "/", len(pro_objects))
    pro = pro_objects[i]

    output = MP(G, pro, maxDepth)



















    """ 
    Output format: 

    - index of pro
    - Total number of paths found
    - Number of selected paths according to multipath settings
    - Reason for failure
    - time of building graph
    - time of strict phase
    - time of best effort phase
    - time of optimization phase
    - total time from start to end
    - The found paths and their latency, see formatting in path_calculator.py bottom of file

    # """ 
    # result = f"{i},{output[0]},{output[1]},{output[2]},{output[3]},{output[4]},{output[5]},{output[6]},{output[7]},{output[8]}\n"

    # results_file = f"{CHOSEN_PATH}/results/output.csv"
    # with open(results_file, "w") as file:
    #     file.write("")

    # with open(results_file, "a") as file:
    #     file.write(result)

