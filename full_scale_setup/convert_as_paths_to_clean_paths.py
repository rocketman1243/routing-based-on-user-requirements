

# ripe/rrc00|5 13830|3356|3491|29386|29256 185.164.248.0/22 i 161.129.152.2

filename = "1000_as_paths.txt"

with open("full_scale_setup/data/" + filename, "r") as input:
    with open("full_scale_setup/data/clean_as_paths.csv", "w") as output:
        for line in input:
            path = line.split(" ")[1].split("|")
            outline = ""
            for i, asn in enumerate(path):
                outline += asn
                if i < len(path) - 1:
                    outline += ","

            outline += "\n"
            output.write(outline)



