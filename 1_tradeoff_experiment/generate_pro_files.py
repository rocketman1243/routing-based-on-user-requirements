import random
import json
import os
import networkx as nx
from generate_internet_scalability_paths import generate_path_with_minimum_length

# Tuning values

# experiment = "as_graph"
# experiment = "as_graph_ber_5"
# experiment = "as_graph_ber_25"
# experiment = "as_graph_ber_500"
# experiment = "as_graph_linear"
# experiment = "as_graph_uniform"
# experiment = "city"
# experiment = "flights"
# experiment = "village"
# experiment = "increasing_grid"
# experiment = "internet_graph_0_25_ber"
experiment = "scalability_internet"

n = 100
best_effort_min_amount = n
best_effort_max_amount = n
nr_of_features = n




num_objects = 10


dry_run = False

requirements = list(range(1, nr_of_features + 1))
max_number_of_strict_requirements = 0
max_nr_geolocations = 0

prefix = "1_tradeoff_experiment/"

###################################33

if dry_run:
    print("DRY RUN")

# Cleanup previous files in directory as the number of objects may be less than before,
# causing dead files from previous runs to still exist

output_path = prefix + "pro_files/" + experiment
if not dry_run and experiment != "increasing_grid" and experiment != "scalability_internet":
    files = os.listdir(output_path)
    for file in files:
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

##################################33

ases = []
with open(prefix + "as_numbers/" + experiment + "_as_numbers.txt", "r") as file:
    for line in file:
        ases.append(line[:-1])
print("generating PROS with ", len(ases), "nodes")

# for internet scalability
edges = []
with open(prefix + "as-links.txt", "r") as file:
    for line in file:
        items = line.split("|")
        edges.append([items[0], items[1]])
G = nx.Graph()
G.add_edges_from(edges)

# Generate random JSON objects
output_objects = []


for index in range(num_objects):

    endpoints = random.sample(ases, 2)

    features = list(range(1,nr_of_features + 1))

    as_source = endpoints[0]
    as_destination = endpoints[1]

    if experiment == "increasing_grid":
        start_index = 90
        start_pro = 100 + start_index
        multiplier = start_pro + 10
        # source_index = multiplier * index
        # destination_index = multiplier * (index + 1)
        # as_source = f"({source_index}, {source_index})"
        as_source = f"({start_index + index}, {0})"
        # as_destination = f"({destination_index}, {destination_index})"
        as_destination = f"({start_index + index}, {multiplier})"

    if experiment == "scalability_internet":

        # 10 through 200 in steps of 10
        length = 10
        print("before path generations")
        # path = generate_path_with_minimum_length(G, length)

        pathLengths = list(nx.shortest_path_length(G))
        print(pathLengths)
        for i in range(len(pathLengths)):
            for j in range(len(pathLengths[i])):
                if pathLengths[i][j] == length:
                    as_source = i
                    as_destination = j



        print("after")
        # as_source = path[0]
        # as_destination = path[-1]


    # Requirements for privacy
    strict_amount = random.randint(0, min(max_number_of_strict_requirements, len(features)))
    strict_requirements = random.sample(features, strict_amount)
    strict_requirements.sort()

    other_requirements = [i for i in requirements if i not in strict_requirements]

    best_effort_amount = random.randint(best_effort_min_amount, best_effort_max_amount)

    best_effort_requirements = random.sample(other_requirements, best_effort_amount)
    best_effort_requirements.sort()

    best_effort_mode = random.choice(["biggest_subset", "ordered_list"])

    geolocation_exclude = []

    path_optimization = "none"

    target_amount_of_paths = 1
    minimum_number_of_paths = 1

    fallback_to_ebgp = "false"

    data = {
        "as_source": as_source,
        "as_destination": as_destination,
        "requirements": {
            "strict": strict_requirements,
            "best_effort": best_effort_requirements,
            "best_effort_mode": best_effort_mode
        },
        "geolocation": {
            "exclude": geolocation_exclude
        },
        "path_optimization": path_optimization,
        "multipath": {
            "target_amount_of_paths": target_amount_of_paths,
            "minimum_number_of_paths": minimum_number_of_paths
        },
        "fallback_to_ebgp_if_no_path_found": fallback_to_ebgp
    }

    output_objects.append(data)

if not dry_run:
    # Print the generated JSON objects
    for i, obj in enumerate(output_objects):
        with open(f"{output_path}/pro_{(i + start_pro):03}.json", "w") as file:
            file.write(f"{json.dumps(obj, indent=2)}")

