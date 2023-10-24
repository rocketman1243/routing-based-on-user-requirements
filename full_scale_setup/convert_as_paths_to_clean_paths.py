

# ripe/rrc00|5 13830|3356|3491|29386|29256 185.164.248.0/22 i 161.129.152.2

filename = "1000_as_paths.txt"

as_numbers = []
with open("full_scale_setup/data/as_numbers.txt", "r") as file:
    for line in file:
        as_numbers.append(line[:-1])

with open("full_scale_setup/data/" + filename, "r") as input:
    with open("full_scale_setup/data/clean_as_paths.csv", "w") as output:
        for line in input:
            path = line.split(" ")[1].split("|")

            skip = False
            for asn in path:
                if asn not in as_numbers:
                    skip = True
                    
            if skip:
                continue

            output_line = ""
            for i, asn in enumerate(path):
                output_line += asn
                if i < len(path) - 1:
                    output_line += ","

            output_line += "\n"
            output.write(output_line)



