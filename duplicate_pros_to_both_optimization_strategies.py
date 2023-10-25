import json
import os
from types import SimpleNamespace




input_path = "full_scale_setup/cost_of_optimization_experiment/unduplicated_pro_files" 

output_path = "full_scale_setup/cost_of_optimization_experiment/pro_files"













# Read in PRO objects   
pro_objects = []

for _, _, filenames in os.walk(f"{input_path}/"):
    filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
    for filename in filenames:
        with open(f"{input_path}/" + filename) as pro_file:
            pro_content = pro_file.read()
            pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
            pro_objects.append(pro_object)



# Generate a copy for each object with both optimization strategies
output_objects = []

for pro in pro_objects:
    for strategy in ["minimize_total_latency", "minimize_number_of_hops"]:
        data = {
            "as_source": pro.as_source,
            "as_destination": pro.as_destination,
            "requirements": {
                "strict": pro.requirements.strict,
                "best_effort": pro.requirements.best_effort,
                "best_effort_mode": pro.requirements.best_effort_mode
            },
            "geolocation": {
                "exclude": pro.geolocation.exclude
            },
            "path_optimization": strategy,
            "multipath": {
                "target_amount_of_paths": pro.multipath.target_amount_of_paths,
                "minimum_number_of_paths": pro.multipath.minimum_number_of_paths
            },
            "fallback_to_ebgp_if_no_path_found": pro.fallback_to_ebgp_if_no_path_found
        }

        output_objects.append(data)

# Print the generated JSON objects
for i, obj in enumerate(output_objects):
    strategy = obj["path_optimization"]
    with open(f"{output_path}/pro_{(i):02}_{strategy}.json", "w") as file:
        file.write(f"{json.dumps(obj, indent=2)}")

