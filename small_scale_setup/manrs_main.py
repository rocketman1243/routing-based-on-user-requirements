from manrs_path_calculator import calculate_paths
import os
import json
from types import SimpleNamespace

# Read in PRO objects
pro_objects = []

for _, _, filenames in os.walk("manrs_pro_files/"):
    for filename in filenames:
        with open("manrs_pro_files/" + filename) as pro_file:
            pro_content = pro_file.read()
            pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
            pro_objects.append(pro_object)

results_file = "manrs_results/proof_of_concept.csv"
with open(results_file, "w") as file:
    file.write("")

for i in range(len(pro_objects)):
    print("pro", i, "/", len(pro_objects))
    pro = pro_objects[i]

    output = calculate_paths("manrs_nio_files/", pro, "non-verbose")
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

    """ 
    result = f"{i},{output[0]},{output[1]},{output[2]},{output[3]},{output[4]},{output[5]},{output[6]},{output[7]}\n"

    with open(results_file, "a") as file:
        file.write(result)

