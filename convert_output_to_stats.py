from statistics import mean, median



def spit_stats(input: list, stat: str):
    min_s = min(input)
    median_s = median(input)
    average_s = round(mean(input))
    max_s = max(input)

    print("stats for : ", stat, ": ", min_s, median_s, average_s, max_s)


# 0,2,2,success,4.63,2.24,4.68,4.89,16.44,204441;48362;2134;7015;55175-112|204441;8437;3320;6461;13977;55175-121

# new:
# 3,2,2,success,5.45,1.41,3.28,4.85,14.99,395994;209;1239;204995-109|395994;33660;3356;204995-112#395994;33660;3356;204995-112


# min, median, average, max of:

# - hop count
# - estimated total latency
# - number of paths

csv_path = "full_scale_setup/initial_results_experiment/results/output.csv"

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


        paths_and_shortest_path = items[len(items) - 1].split("#")
        paths_and_latency = paths_and_shortest_path[0].split("|")
        
        for path_and_latency in paths_and_latency:
            path = path_and_latency.split("-")[0].split(";")
            latency = path_and_latency.split("-")[1]

            hopcounts.append(len(path))
            latencies.append(int(latency))

        # Cost of control experiment
        shortest_path_no_requirements = paths_and_shortest_path[1]
        sp_path = shortest_path_no_requirements.split("-")[0].split(";")
        sp_latency = int(shortest_path_no_requirements.split("-")[1])
        sp_nr_hops = len(sp_path)

        total_runtimes.append(items[8])
        min_nr_hops_with_requirements = min(hopcounts)
        min_latency_with_requirements = min(latencies)
        extra_hops_due_to_requirements.append(min_nr_hops_with_requirements - sp_nr_hops)
        extra_latency_due_to_requirements.append(min_latency_with_requirements - sp_latency)


print("fails: ", fails)
print("nr_of_paths: ", number_of_paths)
print("hopcounts: ", hopcounts)
print("latencies:", latencies)
print("total runtimes: ", total_runtimes)


print("#fails: ", fails)
spit_stats(number_of_paths, "number_of_paths")
spit_stats(hopcounts, "hopcounts")
spit_stats(latencies, "latencies")