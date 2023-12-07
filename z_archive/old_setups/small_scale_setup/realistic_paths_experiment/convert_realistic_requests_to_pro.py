import csv
import random
import json

filename = "realistic_path_requests.csv"

pro_objects = []

with open(filename, "r") as file:
    reader = csv.DictReader(file)

    for i, line in enumerate(reader):
        requirements = []

        strict_requirements = []
        requirements = ["filtering", "anti_spoofing", "coordination", "routing_information"]
        for req in requirements:
            if line[req] == "yes":
                strict_requirements.append(req)

        other_requirements = [i for i in requirements if i not in strict_requirements]
        best_effort_requirements_amount = random.randint(min(len(other_requirements), 0), len(other_requirements))
        best_effort_requirements = random.sample(other_requirements, best_effort_requirements_amount)

        geolocations_to_exclude = []
        if line["countries_to_exclude"] is not None:
            geolocations_to_exclude = line["countries_to_exclude"].split(";")

        best_effort_mode = random.choice(["biggest_subset", "ordered_list"])

        path_optimization = random.choice(["minimize_total_latency", "minimize_number_of_hops", "none"])
        
        target_amount_of_paths = random.choice([1])
        minimum_number_of_paths = 1

        fallback_to_ebgp = random.choice(["true", "false"])

        pro = {
            "user_story": line["user_story"],
            "as_source": line["from_as"],
            "as_destination": line["to_as"],
            "requirements": {
                "strict": strict_requirements,
                "best_effort": best_effort_requirements,
                "best_effort_mode": best_effort_mode
            },
            "geolocation": {
                "exclude": geolocations_to_exclude
            },
            "path_optimization": path_optimization,
            "multipath": {
                "target_amount_of_paths": target_amount_of_paths,
                "minimum_number_of_paths": minimum_number_of_paths
            },
            "fallback_to_ebgp_if_no_path_found": fallback_to_ebgp
        }

        pro_objects.append(pro)
        
# Write the generated JSON objects to a file
for i, obj in enumerate(pro_objects):
    with open(f"pro_files/pro_{i:02}.json", "w") as file:
        file.write(f"{json.dumps(obj, indent=2)}")

