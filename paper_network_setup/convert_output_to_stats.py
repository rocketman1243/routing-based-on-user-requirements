from statistics import mean, median
import matplotlib.pyplot as plt
import numpy as np
import math

def graphMe(xTicks, yValues, yCap, yValues2, yCap2, xLabel, yLabel, yLabel2, title):
    plt.rcParams["font.family"] = "monospace"

    fig, ax1 = plt.subplots()

    ax1_colour = (0.99, 0.32, 0.32)
    ax1.set_xlabel(xLabel, fontsize=12)
    ax1.set_ylabel(yLabel, fontsize=12)
    ax1.set_yticks(range(0, yCap + 1, 1))
    ax1.plot(range(len(xTicks)), yValues, color=ax1_colour, label=yLabel)
    ax1.set_ylim([0, yCap])

    if len(yValues2) > 0:
        ax1.tick_params(axis='y', labelcolor=ax1_colour)

        yticklabels = []
        yticks = range(0, yCap2 + 1, 10)
        for yt in yticks:
            yticklabels.append(f"{yt}%")
        ax2_colour = (0.22, 0.3, 0.9)
        ax2 = ax1.twinx()
        ax2.plot(yValues2, color=ax2_colour)
        ax2.set_ylabel(yLabel2, color=ax2_colour, fontsize=12)
        ax2.set_yticks(yticks, labels=yticklabels)
        ax2.tick_params(axis='y', labelcolor=ax2_colour)
        ax2.set_ylim([0, yCap2])

    plt.xticks(range(len(xTicks)), xTicks)

    plt.xlim(0, len(xTicks))
    # plt.ylim(0, yCap)



    ax1.set_title(title)

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
            "avg_relative_improvement": float(items[3]) * 100,
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
# - How significant this improvement is (using the relative improvement as indicator somehow)

graphMe(xTicks, avg_improvements, int(math.ceil(max(avg_improvements))), avg_relative_improvements, 100, "[depthLimit, neighbourLimit]", "average number of extra BER","average improvement of # satisfied BER over #BER of initial shortest path (%)","average extra #BER on top of shortest path due to updating path with detours")



# - How limits change average runtime
graphMe(xTicks, avg_runtimes, 10, [], 0, "[depthLimit, neighbourLimit]", "average runtime (s)","","average runtime (s)")


