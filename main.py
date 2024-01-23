from path_calculator import localSearchHeuristic, globalBFS
import os
import json
from types import SimpleNamespace
import networkx as nx
import signal
import time

##########################################################################
### 0. Preamble, change folder paths and flags here if necessary #########
##########################################################################

# Spit output to terminal instead of writing into file
printInsteadOfWriteToFile = True

# enable or disable status print messages
verbose = True

limit_stage_path = "1_limit_stage"
comparison_stage_path = "2_comparison_stage"

##########################################################################
############# 1. Tweak Limits ############################################
##########################################################################

# Tweaking limits is done by creating a list of [depthLimit, neighbourLimit] entries
# Either select multiple entries to compare them (in the limit stage), or
#   select the best set of limits and compare the heuristic performance
#   with these limits to the performance of globalBFS (in the comparison stage)

as_graph_limits = []
as_graph_limits += [[1, i] for i in [10, 20, 30, 40, 50]]
as_graph_limits += [[2, i] for i in [1, 2, 3, 4, 5, 6, 7]]
as_graph_limits += [[3, i] for i in [1, 2, 3]]
as_graph_limits += [[4, i] for i in [1, 2, 3, 4]]

# as_graph_limits = [[2, 3]] # BEST LIMITS

city_limits = [[1, i] for i in [1, 2, 3]]
city_limits = [[2, i] for i in [1, 2, 3]]
city_limits += [[3, i] for i in [1, 2, 3]]
city_limits += [[4, i] for i in [1, 2]]

# city_limits = [[2, 3]] # BEST LIMITS

flights_limits = []
flights_limits += [[1, i] for i in [30, 40, 50, 60]]
flights_limits += [[2, i] for i in [20, 25, 30, 35, 40, 45, 50]]
flights_limits += [[2, i] for i in [31, 32, 33, 34]]
flights_limits += [[3, i] for i in [10, 15, 20, 25]]
flights_limits += [[3, i] for i in [1, 2, 3, 4, 5]]

# flights_limits = [[2, 30]]  # BEST LIMITS


village_limits = []
village_limits += [[11, i] for i in [1, 2, 3, 4, 5, 6, 7, 8]]
village_limits += [[i, 3] for i in [9, 10, 11, 12, 13, 14, 15, 16]]

# village_limits = [[14, 3]] # BEST LIMITS


increasing_grid_limits = [[2, 3]]


internet_graph_0_25_ber_limits = []
internet_graph_0_25_ber_limits += [[1, i] for i in [10, 20, 30, 40, 50]]
internet_graph_0_25_ber_limits += [[2, i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
internet_graph_0_25_ber_limits += [[3, i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
internet_graph_0_25_ber_limits += [[4, i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]


ratio_limits = []
ratio_limits += [[1, i] for i in [10, 20, 30, 40, 50]]
ratio_limits += [[2, i] for i in [11, 12, 13, 14]]
ratio_limits += [[3, i] for i in [1, 2, 3, 4, 5]]
ratio_limits += [[4, i] for i in [1, 2, 3]]

##########################################################################
############# 2. Select experiments ######################################
##########################################################################

experiments = ["as_graph", "city", "flights", "village"]

##########################################################################
############# 3. Select limit or comparison stage ########################
##########################################################################

CHOSEN_PATH = limit_stage_path
# CHOSEN_PATH = comparison_stage_path

##########################################################################
############# 4. Select experiment #######################################
##########################################################################

enableHeuristic = True
enableGlobalBFS = False

##########################################################################
############# 5. Optional: Run test ######################################
##########################################################################

# Uncomment below lines to run test graph instead of selected experiments.

# test_path = "test_files"
# test_nio_path = "test_files/nio_files/"
# CHOSEN_PATH = test_path
# path_to_nio_files = test_nio_path

###########################################################################
###########################################################################

## After setting the correct values above, the correct experiments,
## input map and input path requests are selected automatically, and
## the results are either written to the terminal or to an appropriately named
## output file in the results folder of the selected stage.

#############################################################################

for experiment in experiments:
    pathToNIOFiles = f"{CHOSEN_PATH}/nio_files/{experiment}/"
    pathToPROFiles = f"{CHOSEN_PATH}/pro_files/{experiment}/"

    limit_entries = []
    if "as_graph" in experiment:
        limit_entries = as_graph_limits
    if experiment == "city":
        limit_entries = city_limits
    if experiment == "flights":
        limit_entries = flights_limits
    if experiment == "village":
        limit_entries = village_limits
    if experiment == "increasing_grid":
        limit_entries = increasing_grid_limits
    if experiment == "internet_graph_0_25_ber":
        limit_entries = internet_graph_0_25_ber_limits
    if "ratio" in experiment:
        limit_entries = ratio_limits
    if len(limit_entries) == 0:
        if verbose:
            print("NO LIMITS RECOGNIZED, EXITING")
        exit(0)

    # Read in path request objects
    pro_objects = []

    for _, _, filenames in os.walk(pathToPROFiles):
        filenames.sort(key=lambda f: int("".join(filter(str.isdigit, f))))
        for filename in filenames:
            with open(pathToPROFiles + filename) as pro_file:
                pro_content = pro_file.read()
                pro_object = json.loads(
                    pro_content,
                    object_hook=lambda pro_content: SimpleNamespace(**pro_content),
                )
                pro_objects.append(pro_object)

    # Read node information objects & build graph
    nio_objects = []
    as_numbers = []
    node_info = {}
    edges = []
    edge_info = {}
    for _, _, files in os.walk(pathToNIOFiles):
        for file in files:
            with open(pathToNIOFiles + file, "r") as nio_file:
                nio_content = nio_file.read()
                nio_object = json.loads(
                    nio_content,
                    object_hook=lambda nio_content: SimpleNamespace(**nio_content),
                )

                as_numbers.append(nio_object.as_number)
                node_info[nio_object.as_number] = {
                    "features": nio_object.features,
                    "filtered": False,
                }
                here = nio_object.as_number
                for index, other in enumerate(nio_object.connections):
                    edges.append([here, other])

    # Build graph
    G = nx.Graph()
    G.add_nodes_from(as_numbers)
    nx.set_node_attributes(G, node_info)
    G.add_edges_from(edges)

    # Find full path

    if not enableGlobalBFS:
        if verbose:
            print("globalBFS is DISABLED!")
    if not enableHeuristic:
        if verbose:
            print("HEURISTIC IS DISABLED!")
    if "comparison" in CHOSEN_PATH and enableGlobalBFS:

        def handler(signum, frame):
            raise Exception("end of time")

        timePerPROSeconds = 300  # 5 minutes = 300 seconds

        if verbose:
            print(
                "Note: FINDING FULL PATH with slowpoke globalBFS. SO settle in cos this is going to take some time....."
            )

        outputFilePathGlobalSearch = f"{CHOSEN_PATH}/results/{experiment}_global.csv"

        # reset file
        open(outputFilePathGlobalSearch, "w")

        for i in range(len(pro_objects)):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timePerPROSeconds)
            if verbose:
                print(f"{experiment} - slowpoke pro:", i)
            try:
                tic = time.time()
                Pb, totalNrOfBER = globalBFS(G, pro_objects[i])
                runtime = time.time() - tic
                with open(outputFilePathGlobalSearch, "a") as file:
                    if printInsteadOfWriteToFile:
                        if verbose:
                            print(f"{i},{len(Pb)},{totalNrOfBER},{round(runtime, 3)}\n")
                    else:
                        file.write(
                            f"{i},{len(Pb)},{totalNrOfBER},{round(runtime, 3)}\n"
                        )
            except Exception as e:
                if verbose:
                    print("too slow:", e)

        # prevent signal from killing heuristic
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(10000000)

    if not enableHeuristic:
        exit(0)

    if verbose:
        print("Finding paths using speedy boiiiiiiiiii heuristic!")

    outputFilePathHeuristic = f"{CHOSEN_PATH}/results/{experiment}_heuristic.csv"

    if "filter" in CHOSEN_PATH:
        # reset results file
        open(outputFilePathHeuristic, "w")

    for current_limits in limit_entries:
        if "comparison" in CHOSEN_PATH:
            outputFilePathHeuristic = (
                f"{CHOSEN_PATH}/results/{experiment}_{current_limits}.csv"
            )
            open(outputFilePathHeuristic, "w")
        with open(outputFilePathHeuristic, "a") as file:
            improvements = []
            relative_improvements = []
            runtimes = []
            pathfinderTimes = []

            if verbose:
                print("current limits:", current_limits, ", map:", experiment)

            for i in range(len(pro_objects)):
                if verbose:
                    print(experiment + " - pro", i)
                pro = pro_objects[i]

                (
                    totalHops,
                    extraHops,
                    totalNrOfBER,
                    improvement,
                    runtime,
                    pathfinderTime,
                ) = localSearchHeuristic(G, pro, current_limits)

                if "comparison" in CHOSEN_PATH:
                    comparison_result_string = (
                        f"{i},{totalHops},{totalNrOfBER},{round(runtime, 3)}\n"
                    )
                    if printInsteadOfWriteToFile:
                        if verbose:
                            print(comparison_result_string)
                    else:
                        file.write(comparison_result_string)

                if verbose:
                    # print("pathfinderTime: ", pathfinderTime)
                    print("total time:", round(runtime, 3))

                runtimes.append(runtime)
                improvements.append(improvement)
                pathfinderTimes.append(pathfinderTime * 1000)

                # Shows you how large the improvement was over the original number of BER,
                # gives insight into the size of the impact (20 improvement over original of 70 is less epic than 20 improvement over original of 10)
                if totalNrOfBER > 0:
                    relative_improvements.append(improvement / totalNrOfBER)
                else:
                    relative_improvements.append(0)

            avg_improvement = round(sum(improvements) / len(improvements), 3)
            avg_relative_improvement = round(
                sum(relative_improvements) / len(relative_improvements), 3
            )
            avg_runtime = round(sum(runtimes) / len(runtimes), 3)
            avg_pathfinder_time = round(sum(pathfinderTimes) / len(pathfinderTimes), 6)

            if verbose:
                print("avg improvement: ", avg_improvement)
                # print("max improvement:", max(improvements))
                print("avg runtime: ", avg_runtime)
                # print("max runtime:", max(runtimes))
                # print("avg pathfinder time (ms):", avg_pathfinder_time)
                # print("-----------------------------")

            # Format runtimes in list-string to reconstruct for a boxplot to show spread of runtimes
            runtime_string = ""
            for r in runtimes:
                runtime_string = runtime_string + str(r) + "-"
            runtime_string = runtime_string[:-1]

            limit_stage_result_string = f"{current_limits[0]},{current_limits[1]},{avg_improvement},{avg_relative_improvement},{avg_runtime},{runtime_string},\n"

            if "filter" in CHOSEN_PATH:
                if printInsteadOfWriteToFile:
                    if verbose:
                        print(limit_stage_result_string)
                else:
                    file.write(limit_stage_result_string)
