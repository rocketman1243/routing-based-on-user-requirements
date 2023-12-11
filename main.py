from path_calculator import MP, globalBFS
import os
import json
from types import SimpleNamespace
import networkx as nx
import signal
import time

# test_path = "test_files"
# test_nio_path = "test_files/nio_files/"
# CHOSEN_PATH = test_path
# path_to_nio_files = test_nio_path

tradeoff_experiment_path = "1_tradeoff_experiment"
comparison_experiment_path = "2_comparison_experiment"

##########################################################################
############# TWEAK HERE #################################################
##########################################################################

# as_graph_depthLimits = [2]
# as_graph_neighbourLimits = [5, 6, 7, 8, 9, 10]
as_graph_limits = [[1, i] for i in [8, 9, 10, 11, 12]]
as_graph_limits += [[2, i] for i in [5, 6, 7, 8, 9, 10, 11, 12]]
as_graph_limits += [[3, i] for i in [1, 2, 3, 4]]


# city_depthLimits = [3]
# city_neighbourLimits = [2, 4, 6, 8, 10]
city_limits = [[2, i] for i in [6, 7, 8, 9, 10]]
city_limits += [[3, i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
city_limits += [[4, i] for i in [1, 2, 3, 4, 5]]


# flights_depthLimits = [2]
# flights_neighbourLimits = [20, 25, 30, 35, 40]
flights_limits = [[1, i] for i in [30, 40, 50, 60]]
flights_limits += [[2, i] for i in [20, 25, 30, 35, 40, 45, 50]]
flights_limits += [[3, i] for i in [10, 15, 20, 25]]



# village_depthLimits = [13, 14, 15]
# village_neighbourLimits = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
village_limits = [[13, i] for i in [6, 7, 8, 9, 10]]
village_limits += [[14, i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
village_limits += [[15, i] for i in [1, 2, 3, 4, 5]]


graphTypes = ["as_graph", "city", "flights", "village"]

# The limits that average runtime <= 500 ms while providing the most benefits
depthLimitsForComparison = [1]
neighbourLimitsForComparison = [1]


CHOSEN_PATH = tradeoff_experiment_path

disableFullSearch = True

###########################################################################
###########################################################################
###########################################################################



for graphType in graphTypes:
    pathToNIOFiles = f"{CHOSEN_PATH}/nio_files/{graphType}/"
    pathToPROFiles = f"{CHOSEN_PATH}/pro_files/{graphType}/"

    outputFilePathHeuristic = f"{CHOSEN_PATH}/results/{graphType}_heuristic.csv"

    if "comparison" in CHOSEN_PATH:
        depthLimits = depthLimitsForComparison
        neighbourLimits = neighbourLimitsForComparison

    limit_entries = []
    if graphType == "as_graph":
        limit_entries = as_graph_limits
    if graphType == "city":
        limit_entries = city_limits
    if graphType == "flights":
        limit_entries = flights_limits
    if graphType == "village":
        limit_entries = village_limits
    if len(limit_entries) == 0:
        print("NO LIMITS RECOGNIZED, EXITING")
        exit(0)



    # Read in PRO objects
    pro_objects = []

    for _, _, filenames in os.walk(pathToPROFiles):
        filenames.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        for filename in filenames:
            with open(pathToPROFiles + filename) as pro_file:
                pro_content = pro_file.read()
                pro_object = json.loads(pro_content, object_hook=lambda pro_content: SimpleNamespace(**pro_content))
                pro_objects.append(pro_object)


    # Read NIO objects & build graph
    nio_objects = []
    as_numbers = []
    node_info = {}
    edges = []
    edge_info = {}
    for _,_,files in os.walk(pathToNIOFiles):
            for file in files:
                with open(pathToNIOFiles + file, "r") as nio_file:
                    nio_content = nio_file.read()
                    nio_object = json.loads(nio_content, object_hook=lambda nio_content: SimpleNamespace(**nio_content))

                    as_numbers.append(nio_object.as_number)
                    node_info[nio_object.as_number] = {
                        "features": nio_object.features,
                        "filtered": False
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

    if disableFullSearch:
        print("globalBFS is DISABLED!")
    if "comparison" in CHOSEN_PATH and not disableFullSearch:
        def handler(signum, frame):
            raise Exception("end of time")

        # timePerPROSeconds = 300 # 5 minutes = 300 seconds
        timePerPROSeconds = 5


        print("Note: FINDING FULL PATH with slowpoke SMARTBFS. SO settle in cos this is going to take some time.....")

        outputFilePathGlobalSearch = f"{CHOSEN_PATH}/results/{graphType}_global.csv"
        with open(outputFilePathGlobalSearch, "w") as file:
            for i in range(len(pro_objects)):

                signal.signal(signal.SIGALRM, handler)
                signal.alarm(timePerPROSeconds)
                # print(f"{graphType} - slowpoke pro:", i)
                try:
                    tic = time.time()
                    Pb, totalNrOfBER = globalBFS(G, pro_objects[i])
                    runtime = time.time() - tic
                    file.write(f"{i},{len(Pb)},{totalNrOfBER},{round(runtime, 3)}\n")
                except Exception as e:
                    print("too slow:", e)











    print("Finding paths using speedy boiiiiiiiiii")

    # reset results file
    open(outputFilePathHeuristic, "w")

    for current_limits in limit_entries:
        with open(outputFilePathHeuristic, 'a') as file:

            improvements = []
            relative_improvements = []
            runtimes = []
            pathfinderTimes = []

            print("current limits:", current_limits, ", map:", graphType)

            for i in range(len(pro_objects)):
                # print(graphType + " - pro", i)
                pro = pro_objects[i]

                totalHops, extraHops, totalNrOfBER, improvement, runtime, pathfinderTime = MP(G, pro, current_limits)

                if "comparison" in CHOSEN_PATH:
                    comparison_result_string = f"{i},{totalHops},{totalNrOfBER},{round(runtime, 3)}\n"
                    file.write(comparison_result_string)

                # print("pathfinderTime: ", pathfinderTime)
                # print("total time:", round(runtime, 3))

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
            avg_relative_improvement = round(sum(relative_improvements) / len(relative_improvements), 3)
            avg_runtime = round(sum(runtimes) / len(runtimes), 3)
            avg_pathfinder_time = round(sum(pathfinderTimes) / len(pathfinderTimes), 6)

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

            tradeoff_result_string = f"{current_limits[0]},{current_limits[1]},{avg_improvement},{avg_relative_improvement},{avg_runtime},{runtime_string},\n"

            if "tradeoff" in CHOSEN_PATH:
                file.write(tradeoff_result_string)

