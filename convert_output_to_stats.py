from statistics import mean, median



def spit_stats(input: list, stat: str):
    min_s = min(input)
    median_s = median(input)
    average_s = round(mean(input), 1)
    max_s = max(input)

    print("stats for : ", stat, ": ", min_s, median_s, average_s, max_s)




# min, median, average, max of:

# - hop count
# - estimated total latency
# - number of paths

csv_path = "full_scale_setup/proof_of_concept_experiment/results/output.csv"

number_of_paths = []
hopcounts = []
latencies = []
fails = 0

total_runtimes = []
extra_hops_due_to_requirements = []
extra_latency_due_to_requirements = []



with open(csv_path, "r") as file:
    for line in file:
        items = line.split(",")

        # Initial results experiment
        if items[3] != "success":
            fails += 1
            continue

        number_of_paths.append(int(items[1]))


        macro_path_separator = items[len(items) - 1].split("#")
        paths_and_latency = macro_path_separator[0].split("|")

        local_hopcounts = []
        local_latencies = []
        
        for path_and_latency in paths_and_latency:
            path = path_and_latency.split("-")[0].split(";")
            path_hopcount = len(path)
            path_latency = int(path_and_latency.split("-")[1])

            local_hopcounts.append(path_hopcount)
            local_latencies.append(path_latency)


        hopcounts.extend(local_hopcounts)
        latencies.extend(local_latencies)

        # Cost of control experiment
        shortest_path_no_requirements = macro_path_separator[1]
        shortest_path_no_requirement_path = shortest_path_no_requirements.split("-")[0].split(";")
        shortest_path_no_requirement_nr_hops = len(shortest_path_no_requirement_path)

        fastest_path_no_requirements = macro_path_separator[2]
        fastest_path_no_requirements_latency = int(fastest_path_no_requirements.split("-")[1])

        total_runtimes.append(float(items[8]))
        
        min_nr_hops_with_requirements = min(local_hopcounts)
        min_latency_with_requirements = min(local_latencies)

        extra_hops_due_to_requirements.append(min_nr_hops_with_requirements - shortest_path_no_requirement_nr_hops)
        extra_latency_due_to_requirements.append(min_latency_with_requirements - fastest_path_no_requirements_latency)


# 1,2,2,success,5.87,1.79,1.38,5.98,15.02,26405;3356;8220;49065-108|26405;13354;49544;49079;49065-106#26405;3356;8220;49065-108#26405;13354;49544;49079;49065-106

# print("fails: ", fails)
# print("nr_of_paths: ", number_of_paths)
# print("hopcounts: ", hopcounts)
# print("latencies:", latencies)
# print("total runtimes: ", total_runtimes)


print("#fails: ", fails, "/", len(total_runtimes))
spit_stats(number_of_paths, "number_of_paths")
spit_stats(hopcounts, "hopcounts")
spit_stats(latencies, "latencies")
spit_stats(total_runtimes, "COC total runtimes")
spit_stats(extra_hops_due_to_requirements, "COC extra hops")
spit_stats(extra_latency_due_to_requirements, "COC extra latency")