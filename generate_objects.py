import random
import json
import as_numbers


# Lists of possible values

as_sources = as_numbers.get_as_numbers()

countries = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW" ]

requirements = range(1, 31)

# Generate random JSON objects
num_objects = 25
output_objects = []

for _ in range(num_objects):
    as_source = random.choice(as_sources)

    new_ases = as_sources 
    new_ases.remove(as_source)
    as_destination = random.choice(new_ases)
    
    strict_amount = random.randint(0, 3)
    strict = random.sample(requirements, strict_amount)
    strict.sort()

    other_requirements = [i for i in requirements if i not in strict]
    best_effort_amount = random.randint(0, 27)
    best_effort = random.sample(other_requirements, best_effort_amount)
    best_effort.sort()
    
    geolocation_amount = random.randint(0, 10)
    geolocation_exclude = random.sample(countries, geolocation_amount)
    geolocation_exclude.sort()
    
    path_optimization = random.choice(["minimize_total_latency", "minimize_number_of_hops", "none"])
    
    target_amount_of_paths = random.randint(1, 6)
    minimum_number_of_paths = random.randint(1, target_amount_of_paths)
    
    best_effort_mode_security = random.choice(["biggest_subset", "ordered_list"])
    best_effort_mode_privacy = random.choice(["biggest_subset", "ordered_list"])
    
    data = {
        "as_source": as_source,
        "as_destination": as_destination,
        "security": {
            "strict": strict,
            "best_effort": best_effort,
            "best_effort_mode": best_effort_mode_security
        },
        "privacy": {
            "strict": strict,
            "best_effort": best_effort,
            "best_effort_mode": best_effort_mode_privacy
        },
        "geolocation": {
            "exclude": geolocation_exclude
        },
        "path_optimization": path_optimization,
        "multipath": {
            "target_amount_of_paths": target_amount_of_paths,
            "minimum_number_of_paths": minimum_number_of_paths
        }
    }
    
    output_objects.append(data)

# Print the generated JSON objects
for i, obj in enumerate(output_objects):
    with open("pro_files/pro_" + str(i+1) + ".json", "w") as file:
        file.write(f"{json.dumps(obj, indent=2)}")

