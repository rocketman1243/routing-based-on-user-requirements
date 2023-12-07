filename = "tradeoff_experiment/edgelists/streets-LARGE"
oldfile = filename + ".csv"
newfile = filename + ".txt"

i = 0
with open(oldfile, "r") as old:
    with open(newfile, "w") as new:
        for line in old:
            if i == 0:
                i += 1
                continue
            items = line.split(",")

            i += 1

            # if i > 10:
            #     break

            # print(items[2], items[3])
            new.write(f"{items[2]} {items[3]}\n")
