import random
import json
import copy
import os

# Tuning values

# experiment = "as_graph"
# experiment = "city"
# experiment = "flights"
experiment = "village"

num_objects = 100
nr_of_features = 100


dry_run = True
if dry_run:
    print("DRY RUN")

requirements = list(range(1, 101))
best_effort_min_amount = 80
best_effort_max_amount = 100
max_number_of_strict_requirements = 0
max_nr_geolocations = 0

prefix = "2_comparison_experiment/"

###################################33

# Cleanup previous files in directory as the number of objects may be less than before,
# causing dead files from previous runs to still exist

output_path = prefix + "pro_files/" + experiment
if not dry_run:
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

# Generate random JSON objects
output_objects = []


for index in range(num_objects):

    endpoints = random.sample(ases, 2)
    features = list(range(1,nr_of_features))

    as_source = endpoints[0]
    as_destination = endpoints[1]

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
        with open(f"{output_path}/pro_{(i):03}.json", "w") as file:
            file.write(f"{json.dumps(obj, indent=2)}")

