from statistics import mean, median
import matplotlib.pyplot as plt
import numpy as np
import math



def spit_stats(x, y, title, xlabel, ylabel, metric):

    plt.rcParams["font.family"] = "monospace"

    fig, ax = plt.subplots()
    # ax.boxplot(x.values())
    # ax.set_xticklabels(x.keys())

    print(y)
    ax.plot(range(len(x)), x, color=(0.99, 0.32, 0.32), label=f"{metric} of globalBFS")
    ax.set_xlabel(xlabel, fontsize=12)
    if len(y) > 0:
        ax.plot(range(len(x)), y, color=(0.1, 0.8, 0.5), label=f"{metric} of heuristic")
        plt.ylim(0, max(x) + 5)
    ax.set_ylabel(ylabel, fontsize=12)

    plt.xlim(0, 100)

    ax.set_title(title)

    fig.tight_layout()
    plt.tight_layout()

    plt.legend(loc="upper left")
    plt.show()



experiment = "village"
pathFullPaths = f"2_comparison_experiment/results/{experiment}_global.csv"
pathHeuristicPaths = f"2_comparison_experiment/results/{experiment}_heuristic.csv"

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

with open(pathHeuristicPaths, "r") as file:
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

for pro in scoreFullPaths:
    hopcountFull.append(scoreFullPaths[pro]["hopcount"])
    nrBERFull.append(scoreFullPaths[pro]["nrBER"])
    runtimeFull.append(scoreFullPaths[pro]["runtime"])

    hopcountHeuristic.append(scoreHeuristicPaths[pro]["hopcount"])
    nrBERHeuristic.append(scoreHeuristicPaths[pro]["nrBER"])
    runtimeHeuristic.append(scoreHeuristicPaths[pro]["runtime"])

    hopcountDiff.append(scoreFullPaths[pro]["hopcount"] - scoreHeuristicPaths[pro]["hopcount"])
    BERdiff.append(scoreFullPaths[pro]["nrBER"] - scoreHeuristicPaths[pro]["nrBER"])

hopcounts = {
    "globally best paths": hopcountFull,
    "heuristic paths": hopcountHeuristic
}
hopcountDiffDict = {
    "global hopcount -- heuristic hopcount": hopcountDiff
}

spit_stats(nrBERFull, nrBERHeuristic, f"Comparison of #BER for the {experiment} graph type.\n\nRed line visible: Globally optimal path satisfies more BER than heuristic path", "path request number", "# satisfied BER", "# satisfied BER")

# spit_stats(runtimeFull, runtimeHeuristic, f"Runtime to find global path much larger than heuristic for the {experiment} graph type.", "path request number", "runtime (seconds)", "runtime (s)")

# spit_stats(hopcountDiff,[], f"Runtime comparison for the {experiment} graph type.\n\nPositive: Global path is longer. Negative: Heuristic path is longer", "", "path request number", "Difference in hopcount")