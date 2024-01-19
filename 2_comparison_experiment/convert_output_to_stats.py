from statistics import mean, median
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.lines import Line2D



# def spit_stats(x, y, title, xlabel, ylabel, metric):

#     plt.rcParams["font.family"] = "monospace"

#     fig, ax = plt.subplots()
#     # ax.boxplot(x.values())
#     # ax.set_xticklabels(x.keys())

#     print(y)
#     ax.plot(range(len(x)), x, color=(0.99, 0.32, 0.32), label=f"{metric} of globalBFS")
#     ax.set_xlabel(xlabel, fontsize=12)
#     if len(y) > 0:
#         ax.plot(range(len(x)), y, color=(0.1, 0.8, 0.5), label=f"{metric} of heuristic")
#         plt.ylim(0, max(x) + 5)
#     ax.set_ylabel(ylabel, fontsize=12)

#     plt.xlim(0, 100)

#     ax.set_title(title)

#     fig.tight_layout()
#     plt.tight_layout()

#     plt.legend(loc="upper left")
#     plt.show()

# def cdf(data, title, xlabel, ylabel):
#     plt.rcParams["font.family"] = "monospace"
#     plt.rcParams["font.size"] = "18"


#     plt.hist(data, color = (0.2, 0.9, 0.2), histtype="barstacked", bins=np.arange(12))
#     plt.yticks(list(range(0, 101, 10)), labels=[str(i) for i in list(range(0, 101, 10))])
#     plt.xticks(list(range(12)))
#     # plt.xlim(0, 11)

#     plt.title(title)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)

#     plt.tight_layout()
#     # plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - comparison experiment/comparison-{experiment}.pdf", bbox_inches="tight")
#     # plt.show()

def boxplotMe(differences, xLabel, yLabel, title):
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["font.size"] = "18"

    fig, ax1 = plt.subplots()
    xdata = range(1, len(differences.keys()) + 1)
    c = "#9ce37d"
    ax1.boxplot(differences.values(),
            notch=True,
            patch_artist=True,
            showmeans=True,
            boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            medianprops=dict(color="orange")
            )

    yline2 = [0.01 for i in xdata]
    ax1.plot(xdata, yline2, linestyle="dashed", label="10 ms", color = "grey")
    yline1 = [0.04 for i in xdata]
    ax1.plot(xdata, yline1, linestyle="dotted", label="40 ms", color = "grey")




    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel)
    ax1.set_title(title)

    plt.legend()

    handles1, labels = ax1.get_legend_handles_labels()
    line = Line2D([0], [0], label='Average value', color='green', linestyle='None', marker="^")
    handles1.extend([line])
    # plt.legend(handles=handles1, loc=(0.005, 0.05))
    plt.legend(handles=handles1, loc="upper left", fontsize = 16)


    fig = plt.gcf()
    fig.set_size_inches(19.5, 9)
    # plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - comparison experiment/{experiment}-comparison.pdf", bbox_inches="tight")

    plt.show()

def playMeSomeViolinPlots(differences, xLabel, yLabel, title, avgRelativeDiffs):
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["font.size"] = "18"

    fig, ax1 = plt.subplots()
    xdata = range(1, len(differences.keys()) + 1)

    c = "#9ce37d"
    violin = ax1.violinplot(differences.values(), showmeans=True,
                     showextrema=True, showmedians=False, widths=0.8)

    for i in range(len(differences)):
        ax1.annotate(
            str(round(avgRelativeDiffs[i])) + "%",
            (i + 1 - 0.2, max(differences[list(differences)[i]]) + 0.2),
            ha="left",
            rotation=0)

    for pc in violin["bodies"]:
        pc.set_facecolor("#7ef77c")
        pc.set_edgecolor("black")
        pc.set_alpha(0.8)

    violin["cmeans"].set_edgecolor("blue")
    # violin["cmedians"].set_edgecolor("red")

    plt.xticks(xdata, labels=differences.keys(), rotation=25)
    ax1.set_xlim([0, len(differences) + 1])
    ax1.set_yticks([i for i in range(0, 26, 2)] + [25], labels=[str(i) for i in range(0, 26, 2)] + [str(25)])
    ax1.set_ylim([-0.25, 25])

    medians = []
    maxes = []
    for r in differences.values():
        medians.append(np.median(r))
        maxes.append(np.max(r))

    yline2 = [2 for i in xdata]
    ax1.plot(xdata, yline2, linestyle="dashed", label="Score difference = 2", color = "grey")
    yline1 = [1 for i in xdata]
    ax1.plot(xdata, yline1, linestyle="dotted", label="Score difference = 1", color = "grey")




    ax1.set_xlabel(xLabel)
    ax1.set_ylabel(yLabel)
    ax1.set_title(title)

    plt.legend()

    handles1, labels = ax1.get_legend_handles_labels()
    line = Line2D([0], [0], label='average value of violin plot', color='blue')
    # line2 = Line2D([0], [0], label='median value of violin plot', color='red')
    handles1.extend([line])
    # plt.legend(handles=handles1, loc=(0.005, 0.05))
    plt.legend(handles=handles1, loc="upper left", fontsize = 16)


    fig = plt.gcf()
    fig.set_size_inches(19.5, 9)
    plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - comparison experiment/{experiment}-comparison.pdf", bbox_inches="tight")

    # plt.show()

# def infrastructure_experiment_limit_values():
#     plt.rcParams["font.family"] = "monospace"
#     plt.rcParams["font.size"] = "18"

#     x = ["AS Graph", "City", "Flights", "Village"]
#     depthLimitValues = [2, 2, 2, 14]
#     neighbourLimitValues = [8, 3, 30, 3]
#     xticks = np.arange(4)

#     x.reverse()
#     neighbourLimitValues.reverse()
#     depthLimitValues.reverse()

#     plt.barh(xticks+0.2, depthLimitValues, color="tab:orange", height=0.4, label="depthLimit")
#     plt.barh(xticks-0.2, neighbourLimitValues, color="tab:green", height=0.4, label="neighbourLimit", hatch="/")
#     plt.title("Limit values for infrastructure experiment", fontsize=18)
#     customXticks = [0, 1, 2, 3, 4, 5, 6, 7, 8] + list(range(10, 33, 2))
#     plt.xticks(customXticks, labels=[str(i) for i in customXticks])
#     plt.yticks(range(4), labels=x)
#     plt.ylabel("Graph type")
#     plt.xlabel("Limit value")
#     plt.legend(loc="upper right")


#     plt.tight_layout()
#     fig = plt.gcf()
#     fig.set_size_inches(11, 3)
#     plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - limit stage/infra-limit-values.pdf", bbox_inches="tight")
#     # plt.show()

def score_range_limit_values():
    plt.rcParams["font.family"] = "monospace"
    plt.rcParams["font.size"] = "18"

    x = ["4-5", "20-25", "80-100", "400-500"]

    depthLimitValues = [3, 2, 2, 2] # variable score range values
    neighbourLimitValues = [6, 15, 8, 3] # variable score range values
    xticks = np.arange(4)

    x.reverse()
    neighbourLimitValues.reverse()
    depthLimitValues.reverse()

    plt.barh(xticks+0.2, depthLimitValues, color="tab:orange", height=0.4, label="depthLimit")
    plt.barh(xticks-0.2, neighbourLimitValues, color="tab:green", height=0.4, label="neighbourLimit", hatch="/")
    plt.title("Limit values for each feature range", fontsize=18)
    customXticks = [0, 1, 2, 3, 4, 5, 6, 7, 8] + list(range(10, 16, 2))
    plt.xticks(customXticks, labels=[str(i) for i in customXticks])
    plt.xlim([0, 16])
    plt.yticks(range(4), labels=x)
    plt.ylabel("Feature range")
    plt.xlabel("Limit value")
    plt.legend(loc="lower right")

    plt.tight_layout()
    fig = plt.gcf()
    fig.set_size_inches(11, 3)
    plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - limit stage/feature-range-limit_values.pdf", bbox_inches="tight")
    # plt.show()

# def ratio_limit_values_bars():
#     plt.rcParams["font.family"] = "monospace"
#     plt.rcParams["font.size"] = "18"

#     x = ["2:3", "3:4", "4:5", "5:6"]

#     depthLimitValues = [2, 2, 2, 2] # variable score range values
#     neighbourLimitValues = [10, 9, 8, 9] # variable score range values
#     xticks = np.arange(4)

#     x.reverse()
#     neighbourLimitValues.reverse()
#     depthLimitValues.reverse()

#     plt.barh(xticks+0.2, depthLimitValues, color="#42a4f5", height=0.4, label="depthLimit")
#     plt.barh(xticks-0.2, neighbourLimitValues, color="#f5bc42", height=0.4, label="neighbourLimit", hatch="x", alpha=.99)
#     plt.title("Limit values for each feature ratio", fontsize=18)
#     customXticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#     plt.xticks(customXticks, labels=[str(i) for i in customXticks])
#     plt.xlim([0, 16])
#     plt.yticks(range(4), labels=x)
#     plt.ylabel("Ratio")
#     plt.xlabel("Limit value")
#     plt.legend(loc="lower right")

#     plt.tight_layout()
#     fig = plt.gcf()
#     fig.set_size_inches(11, 3)
#     plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - limit stage/ratios-limit-values.pdf", bbox_inches="tight")
#     # plt.show()

# def bar():
#     plt.rcParams["font.family"] = "monospace"
#     plt.rcParams["font.size"] = "18"

#     # Feature ranges
#     # x = ["4-5", "20-25", "80-100", "400-500"]
#     # y = [97.80, 98.83, 98.79, 97.14]
#     # different graph types
#     x = ["AS Graph", "City", "Flights", "Village"]
#     # y = [98.79, 85.11, 98.43, 90.28]
#     # selected limit values
#     # x = ["4-5", "20-25", "80-100", "400-500"]

#     # depthLimitValues = [3, 2, 2, 2] # variable score range values
#     # neighbourLimitValues = [6, 15, 8, 2] # variable score range values
#     depthLimitValues = [2, 2, 2, 14]
#     neighbourLimitValues = [8, 3, 30, 3]
#     xticks = np.arange(4)

#     x.reverse()
#     neighbourLimitValues.reverse()
#     depthLimitValues.reverse()

#     # bar_colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
#     # bar_colors = ['tab:orange', 'tab:blue', 'tab:green', 'tab:red']
#     # bar_colors.reverse()
#     # plt.barh(x, y, color=bar_colors)
#     plt.barh(xticks+0.2, depthLimitValues, color="tab:orange", height=0.4, label="depthLimit")
#     plt.barh(xticks-0.2, neighbourLimitValues, color="tab:green", height=0.4, label="neighbourLimit", hatch="/")
#     plt.title("Limit values for infrastructure experiment", fontsize=18)
#     # plt.xticks(range(0, 101, 10), labels=[str(i) + "%" for i in range(0, 101, 10)])
#     customXticks = [0, 1, 2, 3, 4, 5, 6, 7, 8] + list(range(10, 33, 2))
#     plt.xticks(customXticks, labels=[str(i) for i in customXticks])
#     # plt.xlim([0, 16])
#     plt.yticks(range(4), labels=x)
#     # plt.ylabel("Feature range")
#     plt.ylabel("Graph type")
#     # plt.xlabel("Score relative to globally optimal score")
#     plt.xlabel("Limit value")
#     plt.legend(loc="upper right")


#     plt.tight_layout()
#     fig = plt.gcf()
#     fig.set_size_inches(11, 3)
#     plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/figs - limit stage/infra-limit-values.pdf", bbox_inches="tight")
    # plt.show()



experiment = "internet_graph_0_25_ber"
graphTitle = "Score differences between heuristic and globally best solution"

# bar()
score_range_limit_values()
# infrastructure_experiment_limit_values()
# ratio_limit_values_bars()

exit(0)

pathFullPaths = f"2_comparison_experiment/results/{experiment}_global.csv"


internet_graph_0_25_ber_limits = [[1, i] for i in [10, 20, 30, 40, 50]]
internet_graph_0_25_ber_limits += [[2, i] for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
internet_graph_0_25_ber_limits += [[3, i] for i in [1, 2, 3]]
internet_graph_0_25_ber_limits += [[4, i] for i in [1, 2]]

differencesDict = {}
avgRelativeDifferences = []
for limit in internet_graph_0_25_ber_limits:
    heuristicPath = f"2_comparison_experiment/results/{experiment}_{limit}.csv"

    scoreFullPaths = {}
    scoreHeuristicPaths = {}

    nrOfItems = 100
    counter = 0
    with open(pathFullPaths, "r") as file:
        for line in file:
            if counter < 100:
                counter += 1
            else:
                break

            items = line.split(",")

            scoreFullPaths[items[0]] = {
                "hopcount": int(items[1]),
                "nrBER": int(items[2]),
                "runtime": float(items[3])
            }

    with open(heuristicPath, "r") as file:
        for line in file:
            items = line.split(",")

            scoreHeuristicPaths[items[0]] = {
                "hopcount": int(items[1]),
                "nrBER": int(items[2]),
                "runtime": float(items[3])
            }

    hopcountFull = []
    hopcountHeuristic = []
    nrBERFull = []
    nrBERHeuristic = []
    runtimeFull = []
    runtimeHeuristic = []

    hopcountDiff = []
    BERdiff = []
    relativeDifferences = []

    for pro in scoreFullPaths:
        hopcountFull.append(scoreFullPaths[pro]["hopcount"])
        nrBERFull.append(scoreFullPaths[pro]["nrBER"])
        runtimeFull.append(scoreFullPaths[pro]["runtime"])

        hopcountHeuristic.append(scoreHeuristicPaths[pro]["hopcount"])
        nrBERHeuristic.append(scoreHeuristicPaths[pro]["nrBER"])
        runtimeHeuristic.append(scoreHeuristicPaths[pro]["runtime"])

        hopcountDiff.append(scoreFullPaths[pro]["hopcount"] - scoreHeuristicPaths[pro]["hopcount"])
        BERdiff.append(scoreFullPaths[pro]["nrBER"] - scoreHeuristicPaths[pro]["nrBER"])

        if scoreFullPaths[pro]["nrBER"] > 0:
            relativeDifferences.append((scoreHeuristicPaths[pro]["nrBER"]) / scoreFullPaths[pro]["nrBER"] * 100)
        else:
            relativeDifferences.append(100)

    avgRelativeDifferences.append(np.average(relativeDifferences))
    relativeDifferences = []

    hopcounts = {
        "globally best paths": hopcountFull,
        "heuristic paths": hopcountHeuristic
    }
    hopcountDiffDict = {
        "global hopcount -- heuristic hopcount": hopcountDiff
    }


    differencesDict[f"[{limit[0]},{limit[1]}]"] = BERdiff




#
# cdf(BERdiff, graphTitle, "BER difference", "# Path Requests")

playMeSomeViolinPlots(differencesDict, "[depthLimit, neighbourLimit]", "Score difference", graphTitle, avgRelativeDifferences)


# print(nrBERFull)
# print(BERdiff)
# print(relativeDifferences)





# OLD stats

# spit_stats(nrBERFull, nrBERHeuristic, f"Comparison of #BER for the {experiment} graph type.\n\nRed line visible: Globally optimal path satisfies more BER than heuristic path", "path request number", "# satisfied BER", "# satisfied BER")

# spit_stats(runtimeFull, runtimeHeuristic, f"Runtime to find global path much larger than heuristic for the {experiment} graph type.", "path request number", "runtime (seconds)", "runtime (s)")

# spit_stats(hopcountDiff,[], f"Runtime comparison for the {experiment} graph type.\n\nPositive: Global path is longer. Negative: Heuristic path is longer", "", "path request number", "Difference in hopcount")

