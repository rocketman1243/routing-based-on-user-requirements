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
    ax1.plot(range(len(xTicks)), yValues, color=ax1_colour, label=yLabel2)
    ax1.set_ylim([0, yCap])

    if len(yValues2) > 0:
        ax1.set_ylabel(yLabel, fontsize=12, color=ax1_colour)

        yticklabels = []
        yticks = range(0, yCap2 + 1, 10)
        for yt in yticks:
            yticklabels.append(f"{yt}%")
        ax2_colour = (0.22, 0.3, 0.9)
        ax2 = ax1.twinx()
        ax2.plot(yValues2, color=ax2_colour, label=yLabel)
        ax2.set_ylabel(yLabel2, color=ax2_colour, fontsize=12)
        ax2.set_yticks(yticks, labels=yticklabels)
        ax2.tick_params(axis='y', labelcolor=ax2_colour)
        ax2.set_ylim([0, yCap2])

        # plt.legend(loc="upper left")

    plt.xticks(range(len(xTicks)), xTicks)

    plt.xlim(0, len(xTicks))



    ax1.set_title(title, fontsize=14)

    fig.tight_layout()
    plt.tight_layout()


    plt.show()

def boxplotMe(runtimes, yLabel, xLabel, title, cap, yValues2, yLabel2):
    plt.rcParams["font.family"] = "monospace"

    fig, ax1 = plt.subplots()
    ax1.boxplot(runtimes.values())
    ax1.set_xticklabels(runtimes.keys())
    ax1.set_xlim([1, len(runtimes) + 1])

    ax1.set_xlabel(xLabel, fontsize=12)
    ax1.set_ylabel(yLabel, fontsize=12)
    ax1.set_title(title, fontsize="14")
    ax1.set_ylim([0, cap])

    if len(yValues2) > 0:
        # ax1_colour = (0.99, 0.32, 0.32)
        # ax1.set_ylabel(yLabel, fontsize=12)

        ax2 = ax1.twinx()
        yticklabels = []

        # yticks = range(0, int(math.ceil(cap)) + 1, 10)
        # for yt in yticks:
        #     yticklabels.append("")
        ax2_colour = (0.22, 0.3, 0.9)
        ax2.plot(yValues2, color=ax2_colour, label=yLabel)
        # ax2.set_ylabel(yLabel2, color=ax2_colour, fontsize=12)
        # ax2.set_yticks(yticks, labels=yticklabels)
        # ax2.tick_params(axis='y', labelcolor=ax2_colour)
        ax2.set_xticks(range(len(runtimes.keys())))
        ax2.set_ylim([0, cap])

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

graphMe(xTicks, avg_improvements, int(math.ceil(max(avg_improvements))), avg_relative_improvements, 100, "[depthLimit, neighbourLimit]", "average number of extra BER","average improvement (%)","average extra #BER on top of shortest path due to updating path with detours")


runtime_threshold = [0.5 for i in range(100)]
runtime_cap = 10
# - How limits change average runtime
graphMe(xTicks, avg_runtimes, runtime_cap, runtime_threshold, runtime_cap, "[depthLimit, neighbourLimit]", "average runtime (s)","","average runtime (s) compared to threshold of 0.5 seconds")

# NOTE: HERE I EDIT DATA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Remove intense outlier to get better view:
new_2_70 = sorted(runtimes_dict["[2, 70]"])
new_2_70.remove(max(new_2_70))
runtimes_dict["[2, 70]"] = new_2_70


# - What range of values the runtimes take on for each set of limits,
boxplot_cap = 0
for key in runtimes_dict:
    if max(runtimes_dict[key]) > boxplot_cap:
        boxplot_cap = max(runtimes_dict[key])

runtime_threshold = [0.5 for i in range(1, len(runtimes_dict) + 3) ]
boxplotMe(runtimes_dict, "runtime (s)", "[depthLimit, neighbourLimit]", "Boxplots of runtimes (s) compared to threshold of 0.5 seconds", boxplot_cap, runtime_threshold, "runtime threshold of 0.5 seconds")


