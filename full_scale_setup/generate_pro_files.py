import random
import json
from find_feasible_paths import generate_valid_pro_data
import copy
import os

# Tuning values

max_number_of_strict_requirements = 0

# Range that best effort requirements can take on, with number of elements per step
best_effort_amount_ranges = [
    [4, 4], 
    [8, 8],
    [12, 12],
    [16, 16],
    [20, 20]
]

number_of_objects_per_best_effort_range = 2

requirements = range(1, 51)

experiment = "scalability_experiment"










###################################33

# Cleanup previous files in directory as the number of objects may be less than before, 
# causing dead files from previous runs to still exist

output_path = experiment + "/pro_files"
files = os.listdir(output_path)
for file in files:
    file_path = os.path.join(output_path, file)
    if os.path.isfile(file_path):
        os.remove(file_path)

# Lists of possible geolocation values
countries = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW" ]


# Generate random JSON objects
output_objects = []


best_effort_ranges = []
for i in range(len(best_effort_amount_ranges)):
    for j in range(number_of_objects_per_best_effort_range):
        best_effort_ranges.append(best_effort_amount_ranges[i])

num_objects = len(best_effort_amount_ranges) * number_of_objects_per_best_effort_range

for index in range(num_objects):

    valid_data = generate_valid_pro_data(experiment)

    endpoints = valid_data[0]
    features = valid_data[1]
    countries_to_not_block = valid_data[2]

    as_source = endpoints[0]
    as_destination = endpoints[1]

    # Requirements for privacy
    strict_amount = random.randint(0, min(max_number_of_strict_requirements, len(features)))
    strict_requirements = random.sample(features, strict_amount)
    strict_requirements.sort()

    other_requirements = [i for i in requirements if i not in strict_requirements]
    best_effort_min_amount = best_effort_ranges[index][0]
    best_effort_max_amount = best_effort_ranges[index][1]
    best_effort_amount = random.randint(best_effort_min_amount, best_effort_max_amount)

    best_effort_requirements = random.sample(other_requirements, best_effort_amount)
    best_effort_requirements.sort()

    best_effort_mode = random.choice(["biggest_subset", "ordered_list"])
    
    geolocation_amount = random.randint(0, 10)
    geolocation_copy = copy.deepcopy(countries)
    for country in countries_to_not_block:
        if country in geolocation_copy:
            geolocation_copy.remove(country)

    geolocation_exclude = random.sample(geolocation_copy, geolocation_amount)
    geolocation_exclude.sort()
    
    path_optimization = random.choice(["minimize_total_latency", "minimize_number_of_hops", "none"])
    
    target_amount_of_paths = random.choice([1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 5, 6])
    minimum_number_of_paths = 1

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

# Print the generated JSON objects
for i, obj in enumerate(output_objects):
    with open(f"{output_path}/pro_{i:02}.json", "w") as file:
        file.write(f"{json.dumps(obj, indent=2)}")

