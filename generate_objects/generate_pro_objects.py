import random
import json
import as_numbers
from find_feasible_paths import generate_valid_pro_data
import copy


# Lists of possible values

as_sources = as_numbers.get_as_numbers()

countries = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW" ]

requirements = range(1, 31)

# Generate random JSON objects
num_objects = 25
min_num_best_effort_reqs = 3
max_num_best_effort_reqs = 8
output_objects = []


for _ in range(num_objects):
    valid_data = generate_valid_pro_data()

    endpoints = valid_data[0]
    privacy_features = valid_data[1]
    security_features = valid_data[2]
    countries_to_not_block = valid_data[3]

    as_source = endpoints[0]
    as_destination = endpoints[1]

    # Requirements for privacy
    privacy_strict_amount = random.randint(0, len(privacy_features))
    privacy_strict = random.sample(privacy_features, privacy_strict_amount)
    privacy_strict.sort()

    privacy_other_requirements = [i for i in requirements if i not in privacy_strict]
    privacy_best_effort_amount = random.randint(min_num_best_effort_reqs, max_num_best_effort_reqs)
    privacy_best_effort_requirements = random.sample(privacy_other_requirements, privacy_best_effort_amount)
    privacy_best_effort_requirements.sort()

    # Requirements for security    
    security_strict_amount = random.randint(0, len(security_features))
    security_strict = random.sample(security_features, security_strict_amount)
    security_strict.sort()

    security_other_requirements = [i for i in requirements if i not in security_strict]
    security_best_effort_amount = random.randint(min_num_best_effort_reqs, max_num_best_effort_reqs)
    security_best_effort_requirements = random.sample(security_other_requirements, security_best_effort_amount)
    security_best_effort_requirements.sort()

    privacy_best_effort_mode = random.choice(["biggest_subset", "ordered_list"])
    security_best_effort_mode = random.choice(["biggest_subset", "ordered_list"])
    
    geolocation_amount = random.randint(0, 10)
    geolocation_copy = copy.deepcopy(countries)
    for country in countries_to_not_block:
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
        "privacy": {
            "strict": privacy_strict,
            "best_effort": privacy_best_effort_requirements,
            "best_effort_mode": privacy_best_effort_mode
        },
        "security": {
            "strict": security_strict,
            "best_effort": security_best_effort_requirements,
            "best_effort_mode": security_best_effort_mode
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
    with open(f"../pro_files/pro_{i:02}.json", "w") as file:
        file.write(f"{json.dumps(obj, indent=2)}")

