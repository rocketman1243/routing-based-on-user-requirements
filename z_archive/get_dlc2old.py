import requests
import json
from api_key import get_bing_apy_key # This key is in a local file. To reproduce, make a free bing maps key at https://www.microsoft.com/en-us/maps/create-a-bing-maps-key and use that to convert address to lat/lon
import geocoder

ases = ['151149', '329250', '329252', '263503', '329243', '151156', '151160', '151148', '151114', '61613', '151166', '151176', '151095', '273756', '151084', '265076', '329247', '273744', '151151', '329254', '151318', '151158', '151077', '151093', '151175', '268524', '61614', '273727']


file = open("asn_data/extra_as_data.csv", "w")
file.write("as_number, country, lat, lon\n")
file.close()
        

bad_nodes = []
bad_addresses = {}

for as_number in ases:
    url = "https://api.bgpview.io/asn/" # + AS number as int

    response = json.loads(requests.get(url + as_number).text)

    country = response["data"]["country_code"]

    address = response["data"]["owner_address"]
    address_as_string = ""

    for i, part in enumerate(address):
        address_as_string += part 
        if i < len(address) - 1:
            address_as_string += ", "

    g = geocoder.bing(address_as_string, key=get_bing_apy_key())
    results = g.json

    if (results is not None):

        lat = results['lat']
        lon = results['lng']

        file_append = open("asn_data/extra_as_data.csv", "a")
        file_append.write(f"{as_number}, {country}, {lat}, {lon}\n")
        file_append.close()

    else:
        bad_nodes.append(as_number)
        bad_addresses[as_number] = {
            "address": address_as_string
        }

file_append.close()

print("bad: ", bad_nodes)