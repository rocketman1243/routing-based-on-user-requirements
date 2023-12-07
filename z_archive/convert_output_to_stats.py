from statistics import mean, median
import matplotlib.pyplot as plt
import numpy as np
import math



def spit_stats(input: list, name: str, xlabel: str, y_values_for_plot = [], ylabel=""):

    fig = plt.figure(figsize=(7.5, 3))
    # fig = plt.figure()

    ax = fig.add_subplot(111)

    if len(y_values_for_plot) == 0:
        ax.boxplot(input, vert=0)
        ax.set_xlabel(xlabel, fontsize=12)
        # ax.set_ylabel(ylabel)
    else:
        ax.plot(input, y_values_for_plot)
        ax.set_xlabel(ylabel, fontsize=12)
        ax.set_ylabel(xlabel, fontsize=12)

    # fig.suptitle('bold figure suptitle', fontsize=14, fontweight='bold')
    ax.set_title(name)

    plt.tight_layout()

    plt.show()





# min, median, average, max of:

# - hop count
# - estimated total latency
# - number of paths

experiment = "scalability_experiment"
csv_path = f"full_scale_setup/{experiment}/results/output.csv"

number_of_paths = []
hopcounts = []
latencies = []
fails = 0

total_runtimes = []
extra_hops_due_to_requirements = []
extra_latency_due_to_requirements = []

as_path_latency_deltas = []
as_path_nr_hops_deltas = []

biggest_subset_number_of_best_effort_requirements = []
biggest_subset_best_effort_runtimes = []
biggest_subset_number_of_subsets = []

ordered_list_number_of_best_effort_requirements = []
ordered_list_best_effort_runtimes = []
ordered_list_number_of_subsets = []

best_effort_mode_is_biggest_subset = True

less_hops_due_to_optimization = []
less_latency_due_to_optimization = []
optimization_phase_min_nr_hops_runtimes = []
optimization_phase_min_latency_runtimes = []
optimization_is_min_latency = True

with open(csv_path, "r") as file:
    for line in file:
        items = line.split(",")

        # Initial results experiment + some setup
        if items[3] != "success":
            fails += 1
            continue

        number_of_paths.append(int(items[1]))


        macro_path_separator = items[9].split("#")
        paths_and_latency = macro_path_separator[0].split("|")

        local_hopcounts = []
        local_latencies = []
        
        for path_and_latency in paths_and_latency:
            path = path_and_latency.split("-")[0].split(";")
            path_hopcount = len(path)
            path_latency = int(path_and_latency.split("-")[1])

            local_hopcounts.append(path_hopcount)
            local_latencies.append(path_latency)


        if experiment == "initial_results_experiment":
            hopcounts.extend(local_hopcounts)
            latencies.extend(local_latencies)


        # Utility variables used multiple times below
        min_nr_hops_with_requirements = min(local_hopcounts)
        min_latency_with_requirements = min(local_latencies)

        # Cost of control experiment
        if experiment == "cost_of_control_experiment":

            shortest_path_no_requirements = macro_path_separator[1]
            shortest_path_no_requirement_path = shortest_path_no_requirements.split("-")[0].split(";")
            shortest_path_no_requirement_nr_hops = len(shortest_path_no_requirement_path)

            fastest_path_no_requirements = macro_path_separator[2]
            fastest_path_no_requirements_latency = int(fastest_path_no_requirements.split("-")[1])

            total_runtimes.append(float(items[8]))
            

            extra_hops_due_to_requirements.append(min_nr_hops_with_requirements - shortest_path_no_requirement_nr_hops)
            extra_latency_due_to_requirements.append(min_latency_with_requirements - fastest_path_no_requirements_latency)

        # Scalability experiment
        if experiment == "scalability_experiment":
            if best_effort_mode_is_biggest_subset:
                biggest_subset_number_of_best_effort_requirements.append(items[10])
                biggest_subset_best_effort_runtimes.append(items[6])
                number_of_subsets = math.pow(2, int(items[10]))
                biggest_subset_number_of_subsets.append(number_of_subsets)

                best_effort_mode_is_biggest_subset = False
            else:
                ordered_list_number_of_best_effort_requirements.append(items[10])
                ordered_list_best_effort_runtimes.append(items[6])
                number_of_subsets = int(items[10])
                ordered_list_number_of_subsets.append(number_of_subsets)

                best_effort_mode_is_biggest_subset = True


        # AS Path experiment
        if experiment == "as_path_experiment":
            best_latency = min(local_latencies)
            best_hopcount = min(local_hopcounts)

            chosen_as_path_latency = items[13] 
            chosen_as_path_nr_hops = items[14]

            as_path_latency_deltas.append(int(chosen_as_path_latency) - best_latency)
            as_path_nr_hops_deltas.append(int(chosen_as_path_nr_hops) - best_hopcount)

        # Cost of optimization experiment
        if experiment == "optimization_trade_off_experiment":
            default_path_nr_hops = int(items[15])
            default_path_latency = int(items[16])

            if optimization_is_min_latency:
                less_latency_due_to_optimization.append(default_path_latency - min_latency_with_requirements)
                optimization_phase_min_latency_runtimes.append(float(items[6]))
                optimization_is_min_latency = False
            else:
                less_hops_due_to_optimization.append(default_path_nr_hops - min_nr_hops_with_requirements)
                optimization_phase_min_nr_hops_runtimes.append(float(items[6]))
                optimization_is_min_latency  = True

        


# this part starts at index 9
# as1;as2;...;asn-latency|as1;as2;...;asn-latency|...|as1;as2;...;asn-latency#shortest;path;no;constraints-latency#fastest;path;no;constraints-latency,NumberOfBestEffortRequirements,BestEffortSubsetGenerationTimeInSeconds,runtime_of_filter,chosen_as_path_latency,chosen_as_path_nr_hops,default_path_nr_hops,default_path_latency

if experiment == "initial_results_experiment":
    print("#fails: ", fails, "/", fails + len(total_runtimes))
    spit_stats(number_of_paths, "Distribution of the number of paths that the path calculator found", "#paths")
    spit_stats(hopcounts, "Distribution of path hopcounts", "#hops")
    spit_stats(latencies, "Distribution of path latencies", "Latency (ms)")
    spit_stats(total_runtimes, "Distribution of path calculator runtimes", "Runtime (seconds)")

if experiment == "cost_of_control_experiment":
    spit_stats(extra_hops_due_to_requirements, "Extra hops caused by having to fulfill user requirements", "Extra #hops")
    spit_stats(extra_latency_due_to_requirements, "Extra latency caused by having to fulfill user requirements", "Extra Latency (ms)")

if experiment == "scalability_experiment":
    spit_stats(biggest_subset_number_of_best_effort_requirements, "Best effort mode runtimes\n(biggest subset mode)", "Runtime of best effort mode (seconds)", biggest_subset_best_effort_runtimes, "# Best effort requirements")
    spit_stats(biggest_subset_number_of_best_effort_requirements, "Best effort: Number of subsets \n(biggest subset mode)", "Number of Subsets", biggest_subset_number_of_subsets, "# Best effort requirements")

    spit_stats(ordered_list_number_of_best_effort_requirements, "Best effort mode runtimes\n(ordered list mode)", "Runtime of best effort mode (seconds)", ordered_list_best_effort_runtimes, "# Best effort requirements")
    spit_stats(ordered_list_number_of_best_effort_requirements, "Best effort: Number of subsets \n(ordered list mode)", "Number of Subsets", ordered_list_number_of_subsets, "# Best effort requirements")

if experiment == "as_path_experiment":
    spit_stats(as_path_latency_deltas, "Extra latency of AS path compared to path calculator path", "Extra Latency (ms)")
    spit_stats(as_path_nr_hops_deltas, "Extra number of hops of AS path compared to path calculator path", "Extra #hops")

if experiment == "optimization_trade_off_experiment":
    spit_stats(less_latency_due_to_optimization, "Difference in latency between default path and optimal path", "Latency (ms)")
    spit_stats(optimization_phase_min_latency_runtimes, "Distribution of optimization phase runtimes\n(Goal: Minimizing latency)", "Runtime (seconds)")
    spit_stats(less_hops_due_to_optimization, "Difference in #hops between default path and optimal path", "#hops")
    spit_stats(optimization_phase_min_nr_hops_runtimes, "Distribution of optimization phase runtimes\n(Goal: Minimizing #hops)", "Runtime (seconds)")