
in_file = open("autnums.txt", "r")

output = open("as_to_country.csv", "w")
output.write("")
output.close()
output = open("as_to_country.csv", "a")


for line in in_file:
    split = line.split()
    asnum = split[0][2:]

    if len(split) == 3:
        country = split[2]
        output.write(f"{asnum},{country}\n")



in_file.close()
output.close()