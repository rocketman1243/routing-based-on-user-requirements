import requests
import json
from api_key import get_bing_apy_key # This key is in a local file. To reproduce, make a free bing maps key at https://www.microsoft.com/en-us/maps/create-a-bing-maps-key and use that to convert address to lat/lon
import geocoder
from progress.bar import Bar
from dlc_1_input import get_dlc1_input


""" 
Strategy:

1. Grab country for each AS from the countries txt file
    - If that file does not contain this AS, add AS to new list and spit that to file
2. Grab average lat/lon for each AS based on COUNTRY
3. Spit (as, country, lat, lon) tuple in dlc_1_output file
4. Rewrite this for the entries not present in countries txt

"""

ases = get_dlc1_input()

output_good = open("asn_data/dlc1_output.csv", "w")
output_good.write("as_number; country; address \n")
output_good.close()
output_good = open("asn_data/dlc1_output.csv", "a")

output_bad = open("dlc_2_input.py", "w")


# Read in country to lat/lon file
country_to_latlon = {}
as_to_country = open("asn_data/as_to_country.txt")

for line in latlon_file:
    els = line.split(",")
    country = els[0]
    lat = els[2]
    lon = els[3]

    country_to_latlon[country] = {
        "lat": lat,
        "lon": lon
    }



# Grab country for each AS, grab associated latlon from locations dict and spit in file
as_country_file = open("asn_data/as_to_country.txt")
as_to_country = {}
bad_ases = []
for line in as_country_file:
    elements = line.split(", ")
    as_number = str(elements[0])
    country = elements[2]

    as_to_country[as_number] = country

for as_number in ases:

    if (as_number not in as_to_country):
        bad_ases.append(as_number)

    country = as_

    latlon = country_to_latlon[as_number]

    output_good.write(f"{as_number},{country},{latlon["lat"]},{latlon["lon"]}\n")

output_good.close()

output_bad.write(f"def get_bad_as_numbers():\n\treturn {bad_ases}")
output_bad.close()





