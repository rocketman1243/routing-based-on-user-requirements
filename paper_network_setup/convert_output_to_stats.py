from statistics import mean, median
import matplotlib.pyplot as plt
import numpy as np
import math

def graphMe(xTicks, yValues, xLabel, yLabel, title):
    plt.rcParams["font.family"] = "monospace"

    fig, ax = plt.subplots()

    ax.plot(range(len(xTicks)), yValues, color=(0.99, 0.32, 0.32), label="UPDATE LABEL IF NEEDED")
    # ax.plot(range(len(avg_relative_improvements) * 100), y, color=(0.1, 0.8, 0.5), label="runtime (s) of heuristic")

    # ax.set_xticklabels(xTicks)
    plt.xticks(range(len(xTicks)), xTicks)
    ax.set_xlabel(xLabel, fontsize=12)
    ax.set_ylabel(yLabel, fontsize=12)

    plt.xlim(0, len(xTicks))
    plt.ylim(0, max(yValues) + 1)



    ax.set_title(title)

    fig.tight_layout()
    plt.tight_layout()

    # plt.legend(loc="upper left")

    plt.show()

def boxplotMe():
    plt.rcParams["font.family"] = "monospace"

    fig, ax = plt.subplots()
    # ax.boxplot(x.values())
    # ax.set_xticklabels(x.keys())

    plt.show()



pathHeuristicPaths = f"paper_network_setup/results/heuristic_paths.csv"

scoreHeuristicPaths = {}

depthLimits = []
neighbourLimits = []

depthLimitDict = {}


with open(pathHeuristicPaths, "r") as file:
    for line in file:
        items = line.split(",")

        depthLimit = items[0]
        neighbourLimit = items[1]

        if depthLimit not in depthLimitDict:
            depthLimitDict[depthLimit] = {}

        depthLimits.append(depthLimit)
        neighbourLimits.append(neighbourLimit)

        runtimes = []
        runtime_string = items[5].split("-")
        for r in runtime_string:
            runtimes.append(float(r))

        neighbourLimitDict = {
            "avg_improvement": float(items[2]),
            "avg_relative_improvement": float(items[3]),
            "avg_runtime": float(items[4]),
            "runtimes": runtimes
        }
        depthLimitDict[depthLimit][neighbourLimit] =  neighbourLimitDict


xTicks = []
avg_improvements = []
avg_relative_improvements = []
avg_runtimes = []

runtimes_dict = {}

# Recombine into mapping of [1,10] : avg_improvements
for depthLimit in depthLimitDict:
    for neighbourLimit in depthLimitDict[depthLimit]:
        xTicks.append(f"[{depthLimit}, {neighbourLimit}]")
        avg_improvements.append(depthLimitDict[depthLimit][neighbourLimit]["avg_improvement"])
        avg_relative_improvements.append(depthLimitDict[depthLimit][neighbourLimit]["avg_relative_improvement"])
        avg_runtimes.append(depthLimitDict[depthLimit][neighbourLimit]["avg_runtime"])
        runtimes_dict[f"[{depthLimit}, {neighbourLimit}]"] = depthLimitDict[depthLimit][neighbourLimit]["runtimes"]

# print(xTicks, avg_improvements,"\n", avg_relative_improvements,"\n", avg_runtimes,"\n", runtimes_dict)

# Graphing part
"""
To show, each in separate pic:

- How limits improve average improvement
- How significant this improvement is (using the relative improvement as indicator somehow)
- How limits change average runtime

- What range of values the runtimes take on for each set of limits,
    and then reason about whether this is acceptable or not (set 500 ms as limit in discussion)



"""

# - How limits improve average improvement

graphMe(xTicks, avg_improvements, "[depthLimit, neighbourLimit]", "average number of extra BER","average extra #BER on top of shortest path due to updating path with detours")

# - How significant this improvement is (using the relative improvement as indicator somehow)




