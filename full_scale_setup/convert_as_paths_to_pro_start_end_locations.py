

# ripe/rrc00|5 13830|3356|3491|29386|29256 185.164.248.0/22 i 161.129.152.2

filename = "1000_as_paths.txt"

with open("full_scale_setup/data/" + filename, "r") as input:
    with open("full_scale_setup/data/as_path_start_end.csv", "w") as output:
        for line in input:
            path = line.split(" ")[1].split("|")
            start = path[0]
            end = path[-1]

            output.write(f"{start},{end}\n")



