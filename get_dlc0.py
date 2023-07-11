import requests
import json
from api_key import get_bing_apy_key # This key is in a local file. To reproduce, make a free bing maps key at https://www.microsoft.com/en-us/maps/create-a-bing-maps-key and use that to convert address to lat/lon
import geocoder
from tqdm import tqdm
from dlc_node_lists import get_dlc_1_nodes


# NODES
nodes = []
node_info = {}

# https://api.asrank.caida.org/dev/docs
asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename, "r")

output_file = open("asn_data/dlc_0.csv", "w")
output_file.write("as_number, country, lat, lon\n")
output_file.close()
output_file = open("asn_data/dlc_0.csv", "a")

dlc_1_nodes = get_dlc_1_nodes()
for line in asn_file:
    asn_object = json.loads(line)
    node = asn_object["asn"] # String datatype
    if (node not in dlc_1_nodes):
        country = asn_object["country"]["iso"]
        lat = asn_object["latitude"]
        lon = asn_object["longitude"]

        # TODO: Check for malformed entries & add them to dlc_1 list
        malformed = False
        if len(country) == 0:
            malformed = True
        if lat == 0 or lon == 0:
            malformed = True

        if (malformed):
            dlc_1_nodes.append(node)
        else:
            output_file.write(f"{node}, {country}, {lat}, {lon}\n")

output_file.close()
asn_file.close()
        
dlc_file = open("asn_data/dlc_1_dump.txt", "w")
dlc_file.write(str(dlc_1_nodes))
dlc_file.close()

