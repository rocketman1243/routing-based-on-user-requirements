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



neighbour_depth_limit = [1]
neighbour_limit = [1, 2, 4, 6]
detour_distance_limit = [2, 3, 4, 5, 6, 7, 8]
limits = [
    neighbour_depth_limit,
    neighbour_limit,
    detour_distance_limit
]


# CHOSEN_PATH = test_path
# path_to_nio_files = test_nio_path

# CHOSEN_PATH = max_best_effort_experiment
# path_to_nio_files = f"{CHOSEN_PATH}/../data/nio_files/"



# CHOSEN_PATH = worst_case_network_path
# CHOSEN_PATH = paper_network_setup_path
CHOSEN_PATH = small_paper_network_setup_path
path_to_nio_files = f"{CHOSEN_PATH}/data/nio_files/"

########################################################################33

# Generate limit entries
limit_entries = []
for i in range(len(limits[0])):
    for j in range(len(limits[1])):
        for k in range(len(limits[2])):
            limit_entries.append([limits[0][i], limits[1][j], limits[2][k]])

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


# Find full path
for i in range(len(pro_objects)):
    print("pro:", i)
    runtime = smartDFS(G, pro_objects[i], len(G.nodes))
    print("runtime:", runtime)
exit(0)



# Reset results file
open(f'{CHOSEN_PATH}/results/output.csv', 'w')

for current_limits in limit_entries:
    improvement_total = 0
    runtime_total = 0
    tree_time_total = 0
    detour_time_total = 0
    augment_time_total = 0

    print("current limits:", current_limits)

    for i in range(len(pro_objects)):
        # print("pro", i + 1, "/", len(pro_objects))
        pro = pro_objects[i]

        improvement, runtime, tree_time, detour_time, augment_time = MP(G, pro, current_limits)

        improvement_total += improvement
        runtime_total += runtime
        tree_time_total += tree_time
        detour_time_total += detour_time
        augment_time_total += (augment_time - detour_time)


    avg_improvement = round(improvement_total / len(pro_objects), 3)
    avg_runtime = round(runtime_total / len(pro_objects), 3)
    avg_treetime = round(tree_time_total / len(pro_objects), 3)
    avg_detour_time = round(detour_time_total / len(pro_objects), 3)
    avg_augment_time = round(augment_time_total / len(pro_objects), 3)

    print("avg improvement: ", avg_improvement)
    print("avg runtime:     ", avg_runtime)
    print("avg tree time:   ", avg_treetime)
    print("avg detour time: ", avg_detour_time)
    print("avg augment time:", avg_augment_time)
    print("-----------------------------")


    # TODO: Spit this into file
    result_string = f"{current_limits[0]},{current_limits[1]},{current_limits[2]},{avg_improvement},{avg_runtime}\n"
    with open(f'{CHOSEN_PATH}/results/output.csv', 'a') as file:
        # for line in results:
        file.writelines(result_string)

