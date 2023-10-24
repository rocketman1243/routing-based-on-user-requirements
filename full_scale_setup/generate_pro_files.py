import random
import json
import copy
import os

# Tuning values

num_objects = 50
experiment = "initial_results_experiment"




dry_run = False
requirements = list(range(1, 31))
best_effort_min_amount = 0
best_effort_max_amount = 5
max_number_of_strict_requirements = 5









########## best effort requirements scalability experiment setup
scalability_experiment = experiment == "scalability_experiment"

# For scalability: Range that best effort requirements can take on, with number of elements per step
# Current setup is 2 PROs with 4 BER, 2 pros with 8 BER, 2 PROs with 12 BER etc.
scalability_best_effort_amounts = [0, 0, 2, 2, 4, 4, 6, 6, 8, 8, 10, 10]

scalability_best_effort_mode_toggle_is_biggest_subset = False # Starts at false s.t. first will be biggest subset
if scalability_experiment:
    num_objects = len(scalability_best_effort_amounts)
    max_number_of_strict_requirements = 0
    scalability_best_effort_mode = "biggest_subset"
    experiment = "scalability_experiment"


############ AS Path comparison setup ##########
as_path_experiment = experiment == "as_path_experiment"
as_paths = []

if as_path_experiment:
    with open("full_scale_setup/data/clean_as_paths.csv", "r") as file:
        for line in file:
            as_paths.append(line)

    with open("full_scale_setup/data/chosen_as_paths.csv", "w") as file:
        file.write("")

###################################33

# Cleanup previous files in directory as the number of objects may be less than before, 
# causing dead files from previous runs to still exist

output_path = ""
if not dry_run:
    output_path = f"full_scale_setup/{experiment}/pro_files"
    files = os.listdir(output_path)
    for file in files:
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

##################################33

ases = []
with open("full_scale_setup/data/as_numbers.txt", "r") as file:
    for line in file:
        ases.append(line[:-1])

# Lists of possible geolocation values
countries = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW" ]


# Generate random JSON objects
output_objects = []





for index in range(num_objects):

    endpoints = random.sample(ases, 2)
    features = list(range(1,31))    

    as_source = endpoints[0]   
    as_destination = endpoints[1]

    if as_path_experiment:
        entry = random.choice(list(range(len(as_paths))))
        as_path = as_paths[entry]

        as_source = as_path.split(",")[0]
        as_destination = as_path.split(",")[-1][:-1]

        with open("full_scale_setup/data/chosen_as_paths.csv", "a") as file:
            file.write(as_path)

    # Requirements for privacy
    strict_amount = random.randint(0, min(max_number_of_strict_requirements, len(features)))
    strict_requirements = random.sample(features, strict_amount)
    strict_requirements.sort()

    other_requirements = [i for i in requirements if i not in strict_requirements]

    if scalability_experiment:
        best_effort_min_amount = scalability_best_effort_amounts[index]
        best_effort_max_amount = scalability_best_effort_amounts[index]

    best_effort_amount = random.randint(best_effort_min_amount, best_effort_max_amount)

    best_effort_requirements = random.sample(other_requirements, best_effort_amount)
    best_effort_requirements.sort()

    best_effort_mode = random.choice(["biggest_subset", "ordered_list"])

    if scalability_experiment and scalability_best_effort_mode_toggle_is_biggest_subset:
        scalability_best_effort_mode_toggle_is_biggest_subset = False
        best_effort_mode = "ordered_list"
    elif scalability_experiment and not scalability_best_effort_mode_toggle_is_biggest_subset:
        scalability_best_effort_mode_toggle_is_biggest_subset = True
        best_effort_mode = "biggest_subset"
    
    geolocation_amount = random.randint(0, 10)
    geolocation_copy = copy.deepcopy(countries)

    geolocation_exclude = random.sample(geolocation_copy, geolocation_amount)
    geolocation_exclude.sort()
    
    path_optimization = random.choice(["minimize_total_latency", "minimize_number_of_hops", "none"])

    if as_path_experiment:
        path_optimization = "minimize_number_of_hops"
    
    target_amount_of_paths = random.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 5, 6])
    minimum_number_of_paths = random.randint(1, target_amount_of_paths)

    fallback_to_ebgp = random.choice(["true", "false"])
    
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
        with open(f"{output_path}/pro_{(i):02}.json", "w") as file:
            file.write(f"{json.dumps(obj, indent=2)}")

