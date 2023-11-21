import random
import json
import copy
import os

# Tuning values

num_objects = 50
# experiment = "max_best_effort_experiment"




dry_run = False

requirements = list(range(1, 101))
best_effort_min_amount = 100
best_effort_max_amount = 100
max_number_of_strict_requirements = 0
max_nr_geolocations = 0

###################################33

# Cleanup previous files in directory as the number of objects may be less than before,
# causing dead files from previous runs to still exist

output_path = ""
if not dry_run:
    output_path = f"paper_network_setup/pro_files"
    files = os.listdir(output_path)
    for file in files:
        file_path = os.path.join(output_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

##################################33

ases = []
with open("paper_network_setup/data/as_numbers.txt", "r") as file:
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

    # Requirements for privacy
    strict_amount = random.randint(0, min(max_number_of_strict_requirements, len(features)))
    strict_requirements = random.sample(features, strict_amount)
    strict_requirements.sort()

    other_requirements = [i for i in requirements if i not in strict_requirements]

    best_effort_amount = random.randint(best_effort_min_amount, best_effort_max_amount)

    best_effort_requirements = random.sample(other_requirements, best_effort_amount)
    best_effort_requirements.sort()

    best_effort_mode = random.choice(["biggest_subset", "ordered_list"])

    geolocation_amount = random.randint(0, max_nr_geolocations)
    geolocation_copy = copy.deepcopy(countries)

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

if not dry_run:
    # Print the generated JSON objects
    for i, obj in enumerate(output_objects):
        with open(f"{output_path}/pro_{(i):02}.json", "w") as file:
            file.write(f"{json.dumps(obj, indent=2)}")

