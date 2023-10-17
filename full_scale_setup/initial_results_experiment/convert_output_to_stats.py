from statistics import mean, median



def spit_stats(input: list, stat: str):
    min_s = min(input)
    median_s = median(input)
    average_s = round(mean(input))
    max_s = max(input)

    print("stats for : ", stat, ": ", min_s, median_s, average_s, max_s)


# 0,2,2,success,4.63,2.24,4.68,4.89,16.44,204441;48362;2134;7015;55175-112|204441;8437;3320;6461;13977;55175-121

# min, median, average, max of:

# - hop count
# - estimated total latency
# - number of paths

csv_path = "full_scale_setup/initial_results_experiment/results/output.csv"

number_of_paths = []
hopcounts = []
latencies = []
fails = 0

with open(csv_path, "r") as file:
    for line in file:
        items = line.split(",")
        if items[3] != "success":
            fails += 1
            continue

        number_of_paths.append(int(items[1]))

        paths_and_latency = items[len(items) - 1].split("|")
        for path_and_latency in paths_and_latency:
            path = path_and_latency.split("-")[0].split(";")
            latency = path_and_latency.split("-")[1]

            hopcounts.append(len(path))
            latencies.append(int(latency))

print("fails: ", fails)
print("nr_of_paths: ", number_of_paths)
print("hopcounts: ", hopcounts)
print("latencies:", latencies)


print("#fails: ", fails)
spit_stats(number_of_paths, "number_of_paths")
spit_stats(hopcounts, "hopcounts")
spit_stats(latencies, "latencies")