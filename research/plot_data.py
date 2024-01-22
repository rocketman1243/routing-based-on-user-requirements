import matplotlib.pyplot as plt
import numpy as np
import math



map = "as_graph"
title = "AS"

###################################3


dataset_degrees = []
generator_degrees = []


with open(f"{map}_dataset_degrees.txt", "r") as file:
    for line in file:
        degree = int(line[:-1])
        dataset_degrees.append(degree)

with open(f"{map}_generator_degrees.txt", "r") as file:
    for line in file:
        degree = int(line[:-1])
        generator_degrees.append(degree)

dataset_degrees.sort(reverse=True)
generator_degrees.sort(reverse=True)

differences = []
xs = min(len(dataset_degrees), len(generator_degrees))
for i in range(xs):
    differences.append(abs(dataset_degrees[i] - generator_degrees[i]))

print(np.average(differences))





plt.rcParams["font.family"] = "monospace"
plt.rcParams["font.size"] = "16"
plt.plot(range(len(dataset_degrees)), dataset_degrees, label="dataset degrees")
plt.plot(range(len(generator_degrees)), generator_degrees, label="generator degrees")
# bottom, top = plt.ylim()
# plt.ylim(0, top)

plt.xlabel("node")
plt.ylabel("degree")
plt.legend()
plt.title(f"Degree distribution comparison plot for the {title} graph")
ax = plt.gca()
ax.set_yscale('log')

# fig = plt.gcf()
# fig.set_size_inches(12, 5)

# plt.savefig(f"/home/timon/Dropbox/Studie/Master/thesis/figures/degree_comparison/{map}_degree_comparison.pdf", bbox_inches="tight")


plt.show()