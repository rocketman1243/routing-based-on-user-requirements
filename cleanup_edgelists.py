filename = "comparison_experiment/edgelists/flights-SMALL"
oldfile = filename + ".csv"
newfile = filename + ".txt"

i = 0
with open(oldfile, "r") as old:
    with open(newfile, "w") as new:
        for line in old:
            if i == 0:
                i += 1
                continue
            items = line.split(" ")

            i += 1

            # if i > 10:
            #     break a

            # print(items[0], items[1])
            new.write(f"{items[0]} {items[1]}\n")
