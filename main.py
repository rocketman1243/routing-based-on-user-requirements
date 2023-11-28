from path_calculator import MP, smartDFS
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
max_best_effort_experiment = "full_scale_setup/max_best_effort_experiment"

paper_network_setup_path = "paper_network_setup"
small_paper_network_setup_path = "small_paper_network_setup"
worst_case_network_path = "worst_case_network_setup"

test_path = "test_files"
test_nio_path = "test_files/nio_files/"

##############################################################################3



# depthLimits = [10]
# neighbourLimits = [5]
# detour_distance_limit = [3]
depthLimits = [3]
neighbourLimits = [5]

limits = [
    depthLimits,
    neighbourLimits
]


CHOSEN_PATH = test_path
path_to_nio_files = test_nio_path





# CHOSEN_PATH = paper_network_setup_path
# # CHOSEN_PATH = small_paper_network_setup_path
# path_to_nio_files = f"{CHOSEN_PATH}/data/nio_files/"

########################################################################33

# Generate limit entries
limit_entries = []
for i in range(len(limits[0])):
    for j in range(len(limits[1])):
        limit_entries.append([limits[0][i], limits[1][j]])

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
                    "features": nio_object.features,
                    "filtered": False
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


# # Find full path
# print("Note: FINDING FULL PATH with SMARTDFS. SO settle in cos this is going to take some time.....")
# for i in range(len(pro_objects)):
#     print("pro:", i)
#     runtime = smartDFS(G, pro_objects[i], len(G.nodes))
#     print("runtime:", runtime)
# exit(0)


print("Finding paths using speedy boiiiiiiiiii")

# Reset results file
open(f'{CHOSEN_PATH}/results/output.csv', 'w')

for current_limits in limit_entries:
    with open(f'{CHOSEN_PATH}/results/output.csv', 'a') as file:

        improvements = []
        runtimes = []

        print("current limits:", current_limits)

        for i in range(len(pro_objects)):
            # print("pro", i + 1, "/", len(pro_objects))
            pro = pro_objects[i]

            extraHops, improvement, runtime = MP(G, pro, current_limits)

            improvements.append(improvement)
            runtimes.append(runtime)


        avg_improvement = round(sum(improvements) / len(improvements), 3)
        avg_runtime = round(sum(runtimes) / len(runtimes), 3)

        print("avg improvement: ", avg_improvement)
        print("max imp:", max(improvements))
        print("avg runtime: ", avg_runtime)
        print("max runtime:", max(runtimes))
        print("-----------------------------")


        # TODO: Spit this into file
        result_string = f"{current_limits[0]},{current_limits[1]},{avg_improvement},{avg_runtime}\n"
        file.write(result_string)

