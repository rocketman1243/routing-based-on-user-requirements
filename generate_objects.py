import random
import json

# Lists of possible values
as_sources = [42614, 48520, 14395, 31660, 207282, 135207, 207242, 272588, 137554, 132581, 146904, 18126, 43406, 27865, 205391, 42118, 264592, 28884, 26396, 7001, 30839, 60884, 45988, 38452, 393283, 206034, 5474, 24298, 39120, 198230, 393510, 39033, 15428, 41649, 203426, 147207, 395474, 47914, 328565, 9211]

strict_lists = [[14], [8], [7], [], [6], [6, 13], [6], [7, 11, 18, 21], [26, 16, 4], [6, 25, 28], [23], [23, 18], [11, 29], [19, 17], [18, 5, 23], [25], [6, 3, 17, 30], [21, 10, 18], [16, 27, 23, 5], [3, 29, 6], [], [19, 7, 1], [15, 11, 25, 2], [17, 11, 14], [], [18, 4, 8, 2], [28, 25, 30, 23], [1, 8, 19, 7], [16], [2, 4, 10, 11], [29, 23, 2], [9, 3, 4], [18, 1, 30], [], [29], [22, 8, 28, 27], [], [], [20, 13, 3], [4, 28, 26, 13]]
best_effort_lists = [[6, 2, 26, 24, 17, 15, 9, 12, 10, 28, 19, 7, 14, 30], [11, 5, 6, 10, 13, 9], [20, 25, 30, 5, 22, 13, 16, 14, 29, 19, 2], [30, 17, 27, 7, 3, 11, 16, 26, 1, 28, 29, 21, 6, 20, 14, 19], [2, 10, 7], [15, 13, 21, 3, 12, 9, 26, 25, 16, 24, 20], [15], [28, 18, 30], [26, 6, 9, 8, 2, 7, 11, 1, 24, 10, 12, 29], [22, 2, 6, 11, 30, 5, 13, 16, 17, 21], [20, 13, 27, 28, 30, 10, 16, 18, 12, 26], [21, 3, 19, 15, 9, 7, 13, 27, 12, 20, 4, 22, 28, 2, 14, 25, 8], [11, 17, 9, 1, 10, 25, 26, 21], [24, 29, 27, 21, 28, 19, 3, 1, 13, 30], [30, 6, 4, 5], [5, 29, 14, 8, 22, 25, 27, 20, 23, 7, 26, 24, 19, 15], [11, 8, 20, 15, 1, 26, 24, 25, 16, 18, 10, 6, 14, 2], [5, 9, 28, 29, 16, 2, 6], [5, 22, 11, 6, 24, 14, 9, 10, 8, 27, 28], [19, 4, 26, 8, 1, 6], [17, 22, 7, 1, 4, 26, 6, 14, 16, 8, 28, 12, 21, 2, 23, 11, 9, 15, 30, 3], [21, 11, 10, 7, 1, 13, 8], [26, 2, 14, 1, 18, 3, 11, 21, 17, 20, 29, 27, 16, 22, 7, 23, 10, 13], [15, 1, 19, 25, 6, 12, 2, 7, 20, 28, 21, 27, 16, 10, 23, 24, 5], [17, 25], [28, 14, 20, 27, 13, 7, 2, 8, 15, 24, 5, 11, 18, 12], [29, 30, 1, 25, 9, 14, 27, 18], [3, 9, 2, 27, 17], [30, 28, 17, 21, 23, 2, 13, 8, 3, 16, 15, 11, 6], [25], [12, 8, 27, 10, 17, 1, 20, 24, 11, 16, 29, 21, 2, 14, 26, 25, 22], [1, 3, 17, 19, 16, 24, 26, 14, 29, 23, 27, 21, 28, 22, 8], [10, 30, 23, 1, 3, 16, 28, 18, 13, 26, 7, 14, 11], [22, 16, 11, 29, 4, 30, 5, 21, 23, 10, 9, 20, 13, 24, 15], [14, 20, 7, 23, 5, 4, 12, 10], [4, 5, 18, 23, 3, 29, 30, 1, 24, 26, 2, 17, 19, 7], [], [16, 28, 19, 7, 2, 14, 22, 30], [18, 24, 2, 10, 27, 29, 6, 25, 16, 21, 5, 26, 1, 14, 30, 15], [25, 16]]

geolocation_exclude_lists = [['EG', 'SR', 'CO', 'AG', 'BT'], ['PN', 'NF', 'IQ', 'PM', 'EC', 'MA'], ['FK', 'ZA', 'LS', 'VN', 'IM'], ['CG', 'SO', 'PW', 'GD', 'RW', 'UG', 'DJ', 'MU', 'MA', 'DE'], ['TN', 'DZ', 'MP', 'PH', 'AZ'], ['FI', 'LU', 'SG', 'QA', 'GU', 'BD', 'TV', 'CH'], ['RU', 'SD', 'BB'], ['DM', 'KM'], ['KE', 'IO', 'IT', 'TN', 'SC', 'PN', 'NP'], ['BS', 'GN', 'KI', 'IM'], ['TJ', 'UM'], ['TO', 'IT', 'IL'], ['SE'], ['NP', 'VG', 'SH', 'BV', 'PN', 'EH', 'IL', 'PG', 'WF', 'HM'], ['EG', 'AT', 'RU', 'WF', 'AG', 'ET', 'GU', 'AO', 'JP'], ['KP', 'HN', 'AT', 'MF', 'PG', 'PL', 'PS', 'AM', 'HK'], ['LU', 'LA', 'BO', 'DM', 'KN', 'KW', 'VN', 'CA', 'DE', 'ME'], ['WF', 'CH', 'GS', 'BW'], ['CH'], ['TR', 'MM', 'TN'], ['EC', 'VU', 'VI', 'JO', 'SV'], ['VE', 'GD', 'US', 'BD', 'IT'], [], ['PT', 'BO', 'GM', 'TN'], ['VE', 'LS']]

# Generate random JSON objects
num_objects = 25
output_objects = []

for _ in range(num_objects):
    as_source = random.choice(as_sources)
    as_destination = random.choice(as_sources)
    
    strict = random.choice(strict_lists)
    best_effort = random.choice([lst for lst in best_effort_lists if not any(item in lst for item in strict)])
    
    geolocation_exclude = random.choice(geolocation_exclude_lists)
    
    path_optimization = random.choice(["minimize_total_latency", "minimize_number_of_hops", "none"])
    
    target_amount_of_paths = random.randint(1, 6)
    minimum_number_of_paths = random.randint(1, target_amount_of_paths)
    
    best_effort_mode = random.choice(["biggest_subset", "ordered_list"])
    
    data = {
        "as_source": as_source,
        "as_destination": as_destination,
        "security": {
            "strict": strict,
            "best_effort": best_effort,
            "best_effort_mode": best_effort_mode
        },
        "privacy": {
            "strict": strict,
            "best_effort": best_effort,
            "best_effort_mode": best_effort_mode
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
for idx, obj in enumerate(output_objects):
    print(f"object {idx}\n{json.dumps(obj, indent=4)}\n")
