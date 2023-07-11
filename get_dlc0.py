import requests
import json
from api_key import get_bing_apy_key # This key is in a local file. To reproduce, make a free bing maps key at https://www.microsoft.com/en-us/maps/create-a-bing-maps-key and use that to convert address to lat/lon
import geocoder


# NODES
nodes = []
node_info = {}

# https://api.asrank.caida.org/dev/docs
asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename)

for line in asn_file:
    asn_object = json.loads(line)
    node = asn_object["asn"] # String datatype
    nodes.append(node)

    info = {
        "country": asn_object["country"]["iso"],
        "lat": asn_object["latitude"],
        "lon": asn_object["longitude"]
    }
    node_info[node] = info

file = open("asn_data/extra_as_data.csv", "w")
file.write("as_number, country, lat, lon\n")
file.close()
        
