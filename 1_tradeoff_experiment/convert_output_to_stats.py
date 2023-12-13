from statistics import mean, median
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.interpolate import make_interp_spline


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





def graphMe(xTicks, yValues0, yValues1, yValues2):
    plt.rcParams["font.family"] = "monospace"

    # make line more smooth
    x = list(range(len(xTicks)))
    X_ = np.linspace(min(x), max(x), 50)
    X_Y0_Spline = make_interp_spline(range(len(xTicks)), yValues0)
    Y0_ = X_Y0_Spline(X_)
    X_Y2_Spline = make_interp_spline(range(len(xTicks)), yValues2)
    Y2_ = X_Y2_Spline(X_)


    plt.plot(range(len(xTicks)), yValues0, color="orange", label="avg runtime")
    # plt.plot(X_, Y0_, color="orange", label="avg runtime")
    plt.plot(range(len(xTicks)), yValues1, linestyle="--", color="orange")
    ax1 = plt.gca()
    plt.xticks(range(len(xTicks)), xTicks)
    ax1.set_xlabel("[depthLimit, neighbourLimit]")
    ax1.set_ylabel("average runtime (ms)", color="orange")
    yticklabels1 = []
    yticks = [i/10 for i in range(0, 12, 1)]
    for yt in yticks:
        yticklabels1.append(str(round(yt * 1000)))
    ax1.set_yticks(yticks, labels=yticklabels1, color="orange")
    ax1.set_ylim(0, 1.15)



    ax2 = ax1.twinx()
    ax2.plot(range(len(xTicks)), yValues2, color="blue")
    # ax2.plot(X_, Y2_, color="blue", label="avg #BER improvement")
    ax2.set_ylabel("#BER improvement", color="blue")
    yticklabels2 = []
    yticks2 = [i for i in range(0, 7, 1)]
    for yt in yticks2:
        yticklabels2.append(str(round(yt)))
    ax2.set_yticks(yticks2, labels=yticklabels2, color="blue")
    ax2.set_ylim(0, 6)

    # mark up the graph for easy readability
    plt.vlines(x = 4, ymin=0, ymax=max(yValues2), color="red")
    plt.vlines(x = 8, ymin=0, ymax=max(yValues2), color="red")
    plt.hlines(y=yValues2[8], xmin=0, xmax=100, color="red", linestyles="dotted")
    plt.vlines(x = 15, ymin=0, ymax=max(yValues2), color="red")
    # plt.axhspan(i, i+.2, facecolor='0.2', alpha=0.5)
    plt.axvspan(0, 8.5, facecolor="green", alpha=0.1)
    plt.axvspan(8.5, 12.5, facecolor="red", alpha=0.1)
    plt.axvspan(12.5, 15.1, facecolor="green", alpha=0.1)
    plt.axvspan(15.1, 16.6, facecolor="red", alpha=0.1)
    plt.axvspan(16.6, 17.9, facecolor="green", alpha=0.1)
    plt.axvspan(17.9, 18, facecolor="red", alpha=0.1)


    # ax1.grid(linestyle='-.')
    plt.tight_layout()
    plt.xlim(0, len(xTicks) - 1)
    # plt.ylim(0, max(yValues2))
    plt.show()

    # yCap = 1
    # fig, ax1 = plt.subplots()

    # ax1_colour = (0.79, 0.32, 0.32)
    # ax1.set_xlabel(xLabel, fontsize=12)
    # ax1.set_ylabel(yLabel, fontsize=12)
    # ax1.set_yticks(range(0, yCap + 1, 1))
    # ax1.plot(range(len(xTicks)), yValues, color=ax1_colour, label=yLabel)
    # ax1.set_ylim([0, yCap])

    # ax1.set_ylabel(yLabel, fontsize=12, color=ax1_colour)

    # # yticklabels = []
    # # yticks = range(0, yCap2 + 1, 10)
    # # for yt in yticks:
    # #     yticklabels.append(f"{yt}%")
    # # ax2.set_yticks(yticks, labels=yticklabels)
    # ax2_colour = (0.22, 0.3, 0.9)
    # ax2 = ax1.twinx()
    # # ax2.plot(yValues2, color=ax2_colour, label=yLabel2, linestyle="dotted")
    # # ax2.tick_params(axis='y', labelcolor=ax2_colour)
    # # ax2.set_ylim([0, yCap2])


    # yticklabels3 = []
    # yticks3 = range(0, yCap3 + 1)
    # for yt in yticks3:
    #     yticklabels3.append(f"{yt}%")
    # ax3_colour = (0.1, 0.5, 0.3)
    # ax3 = ax1.twinx()
    # ax3.plot(yValues3, color=ax3_colour, label=yLabel3)
    # # ax2.set_ylabel(yLabel2, color=ax2_colour, fontsize=12)
    # # ax2.set_yticks(yticks, labels=yticklabels)
    # # ax2.tick_params(axis='y', labelcolor=ax2_colour)
    # # ax2.set_ylim([0, yCap2])


    # plt.legend(loc="upper left")

    # plt.xticks(range(len(xTicks)), xTicks)

    # plt.xlim(0, len(xTicks))



    # ax1.set_title(title, fontsize=14)

    # fig.tight_layout()
    # plt.tight_layout()


    # plt.show()


experiment = "as_graph"
pathHeuristicPaths = f"1_tradeoff_experiment/results/{experiment}_heuristic.csv"

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
            if "e" in r:
                r = "0.00001"
            if r != "05":
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

# graphMe(xTicks, avg_improvements, int(math.ceil(max(avg_improvements))), avg_relative_improvements, 100, "[depthLimit, neighbourLimit]", "average number of extra BER","average improvement (%)","average extra #BER on top of shortest path due to updating path with detours")


runtime_threshold = [0.5 for i in range(len(xTicks))]
runtime_cap = math.ceil(max(avg_runtimes))

# - What set of limits provides the best tradeoff between runtime and improvements?
graphMe(xTicks, avg_runtimes, runtime_threshold, avg_improvements)


# - What range of values the runtimes take on for each set of limits,
# boxplot_cap = 0
# for key in runtimes_dict:
#     if max(runtimes_dict[key]) > boxplot_cap:
#         boxplot_cap = max(runtimes_dict[key])

# runtime_threshold = [0.5 for i in range(1, len(runtimes_dict) + 3) ]
# boxplotMe(runtimes_dict, "runtime (s)", "[depthLimit, neighbourLimit]", "Boxplots of runtimes (s) compared to threshold of 0.5 seconds", boxplot_cap, runtime_threshold, "runtime threshold of 0.5 seconds")


