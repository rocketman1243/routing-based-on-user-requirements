from statistics import mean, median
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
import numpy as np
import math
from scipy.interpolate import make_interp_spline
import csv


def boxplotMe(runtimes, yLabel, xLabel, title, cap, yValues2, yLabel2):
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["font.size"] = "18"

    fig, ax1 = plt.subplots()
    c = "orange"
    ax1.boxplot(runtimes.values(), notch=True, patch_artist=True,
            boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color="green"),
            )
    ax1.set_xticklabels(runtimes.keys())
    print(runtimes.keys())
    ax1.set_xlim([0, len(runtimes) + 1])

    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel)
    ax1.set_title(title)
    ax1.set_ylim([0, cap + 0.25])

    # if len(yValues2) > 0:
    #     # ax1_colour = (0.99, 0.32, 0.32)
    #     # ax1.set_ylabel(yLabel, fontsize=12)

    #     ax2 = ax1.twinx()
    #     yticklabels = []

    #     # yticks = range(0, int(math.ceil(cap)) + 1, 10)
    #     # for yt in yticks:
    #     #     yticklabels.append("")
    #     ax2_colour = (0.22, 0.3, 0.9)
    #     ax2.plot(yValues2, color=ax2_colour, label=yLabel)
    #     # ax2.set_ylabel(yLabel2, color=ax2_colour, fontsize=12)
    #     # ax2.set_yticks(yticks, labels=yticklabels)
    #     # ax2.tick_params(axis='y', labelcolor=ax2_colour)
    #     ax2.set_xticks(range(len(runtimes.keys())))
    #     ax2.set_ylim([0, cap])

    # plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - tradeoff experiment/{experiment}.pdf", bbox_inches="tight")

    plt.show()





def graphMe(xTicks, yValues0, yValues1, yValues2, experiment):
    # plt.rcParams["font.family"] = "monospace"
    # plt.rcParams["font.size"] = "18"
    ax2ylim = 1
    ax2ylimStep = 1
    bestX = 5
    legendLocation = "upper left"
    zoneBoundaries = [5.07]


    # with open("1_tradeoff_experiment/annotation_parameters.csv", "r") as file:
    #     for line in csv.DictReader(file):
    #         if line["graphType"] == experiment:
    #             ax2ylim = int(line["ax2ylim"])
    #             ax2ylimStep = int(line["ax2ylimStep"])
    #             bestX = int(line["bestX"])
    #             legendLocation = line["legendLocation"]
    #             zoneBoundariesString = line["zoneBoundaries"].split("-")
    #             zoneBoundaries = [float(x) for x in zoneBoundariesString]



    plt.rcParams["font.family"] = "monospace"

    orangeColour = "orange"
    plot0 = plt.plot(range(len(xTicks)), yValues0, color=orangeColour, label="avg runtime", linestyle="dashdot")
    plot1 = plt.plot(range(len(xTicks)), yValues1, linestyle="dashed", color=orangeColour, label="maximum allowed runtime")
    ax1 = plt.gca()
    plt.xticks(range(len(xTicks)), xTicks, fontsize=14)
    ax1.set_xlabel("[depthLimit, neighbourLimit]", fontsize=14)
    ax1.set_ylabel("average runtime (ms)", color=orangeColour, fontsize=14)
    yticklabels1 = []
    yticks = [i/10 for i in range(0, 30, 1)]
    for yt in yticks:
        yticklabels1.append(str(round(yt * 1000)))
    ax1.set_yticks(yticks, labels=yticklabels1, color=orangeColour, fontsize = 14)
    ax1.set_ylim(0, 1.2)



    ax2 = ax1.twinx()
    plot2 = ax2.plot(range(len(xTicks)), yValues2, color="blue", label="avg score improvement (right axis)", linestyle="solid")
    # ax2.plot(X_, Y2_, color="blue", label="avg #BER improvement")
    ax2.set_ylabel("average score improvement", color="blue", fontsize=14)



    yticklabels2 = []
    yticks2 = [i/10 for i in range(11)]
    for yt in range(11):
        yticklabels2.append(str(yt / 10))
    ax2.set_yticks(yticks2, labels=yticklabels2, color="blue", fontsize = 14)
    ax2.set_ylim(0, ax2ylim)


    # mark up the graph for easy readability
    greenColour = "green"
    greenAlpha = 0.25
    redColour = "red"
    redAlpha = 0.2
    if len(zoneBoundaries) > 0:
        plt.axvspan(0, zoneBoundaries[0], facecolor=greenColour, alpha=greenAlpha)
        nextIsGreen = False
        if len(zoneBoundaries) > 1:
            for i in range(len(zoneBoundaries) - 1):
                nextColor = redColour
                nextAlpha = redAlpha
                if nextIsGreen:
                    nextColor = greenColour
                    nextAlpha = greenAlpha
                    nextIsGreen = False
                else:
                    nextIsGreen = True
                plt.axvspan(zoneBoundaries[i], zoneBoundaries[i + 1], facecolor=nextColor, alpha=nextAlpha)
        if nextIsGreen:
            plt.axvspan(zoneBoundaries[-1], 10000, facecolor=greenColour, alpha=greenAlpha)
        else:
            plt.axvspan(zoneBoundaries[-1], 10000, facecolor=redColour, alpha=redAlpha)

    vline_colour = (1, 0.2, 0.0)
    plt.vlines(x = bestX, ymin=0, ymax=1200, color=vline_colour, linestyle=(0, (3, 5, 1, 5, 1, 5)), label="best limits")
    plt.hlines(y=yValues2[bestX], xmin=0, xmax=100, color=vline_colour, linestyles=(0, (1, 7)), label="avg improvement of best limits")

    vline_linestyle = (1, (3, 6))
    # plt.vlines(x = 15, ymin=0, ymax=1200, color=vline_colour, linestyle=vline_linestyle)
    # plt.vlines(x = bestX, ymin=0, ymax=1200, color=vline_colour, linestyle=vline_linestyle, label="start of plateau")


    # ax1.grid(linestyle='-.')
    plt.tight_layout()
    plt.xlim(0, len(xTicks) - 1)


    handles1, labels = ax1.get_legend_handles_labels()
    handles2, labels = ax2.get_legend_handles_labels()
    patchGreen = mpatches.Patch(color=greenColour, alpha=greenAlpha, label='fast enough')
    patchRed = mpatches.Patch(color=redColour, alpha=redAlpha, label='too slow')
    # line = Line2D([0], [0], label='manual line', color='k')
    handles1.extend([patchGreen, patchRed])
    handles1.extend(handles2)
    # plt.legend(handles=handles1, loc=(0.005, 0.05))
    plt.legend(handles=handles1, loc=legendLocation, fontsize = 14)




    # plt.legend(loc="upper left")

    ax1.set_title(f"Score improvement and runtime per limit for the {experiment} graph type", fontsize = 18)

    # fig.tight_layout()
    plt.tight_layout()


    plt.show()


experiment = "village"
pathHeuristicPaths = f"1_tradeoff_experiment/results/{experiment}_heuristic.csv"
# pathHeuristicPaths = f"1_tradeoff_experiment/results/{experiment}_heuristic_neighbours_upper_limit.csv"

depthLimits = []
neighbourLimits = []

depthLimitDict = {}

# increasing_depths_runtime_dict = {}
# for i in range(10, 201, 10):
#     increasing_depths_runtime_dict[i] = []

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

        # for i in range(10, 201, 10):
        #     # print("i:", i)
        #     for j in range(i):
        #         index = i - 10 + j
        #         increasing_depths_runtime_dict[i].append(runtimes[j])



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

runtime_dict = {}

# Recombine into mapping of [1,10] : avg_improvements
for depthLimit in depthLimitDict:
    for neighbourLimit in depthLimitDict[depthLimit]:
        xTicks.append(f"[{depthLimit}, {neighbourLimit}]")
        avg_improvements.append(depthLimitDict[depthLimit][neighbourLimit]["avg_improvement"])
        avg_relative_improvements.append(depthLimitDict[depthLimit][neighbourLimit]["avg_relative_improvement"])
        avg_runtimes.append(depthLimitDict[depthLimit][neighbourLimit]["avg_runtime"])
        runtime_dict[f"[{depthLimit}, {neighbourLimit}]"] = depthLimitDict[depthLimit][neighbourLimit]["runtimes"]

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

# # - What set of limits provides the best tradeoff between runtime and improvements?
graphMe(xTicks, avg_runtimes, runtime_threshold, avg_improvements, experiment)


# - What range of values the runtimes take on for each set of limits,
# boxplot_cap = 0
# for key in increasing_depths_runtime_dict:
#     if max(increasing_depths_runtime_dict[key]) > boxplot_cap:
#         boxplot_cap = max(increasing_depths_runtime_dict[key])

# runtime_threshold = [0.5 for i in range(1, len(increasing_depths_runtime_dict) + 3) ]
# boxplotMe(increasing_depths_runtime_dict, "runtime (s)", "#hops between start and end node", "Boxplots of runtimes (s) for increasing hop lengths on grid graph", boxplot_cap, runtime_threshold, "runtime threshold of 0.5 seconds")


