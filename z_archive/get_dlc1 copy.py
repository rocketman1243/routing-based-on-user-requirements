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

def get_country_and_address(as_number: str):
    url = "https://api.bgpview.io/asn/" # + AS number as int

    response = json.loads(requests.get(url + as_number).text)

    country = response["data"]["country_code"]
    address = response["data"]["owner_address"]
    address_as_string = ""

    for i, part in enumerate(address):
        address_as_string += part 
        if i < len(address) - 1:
            address_as_string += ", "

    return (country, address_as_string)

# run this later
def get_lat_lon_from_address(as_number, country, address: str):
    g = geocoder.bing(address_as_string, key=get_bing_apy_key())
    results = g.json

    if results is not None:
        lat = results['lat']
        lon = results['lng']
        return (lat, lon)
    else:
        g = geocoder.bing(country, key=get_bing_apy_key())

        if results is not None:
            lat = results['lat']
            lon = results['lng']
            return (lat, lon)

        else:
            output_bad.write(f"{as_number}, {country} \n")




bar = Bar("addresses", max = len(ases))
for as_number in ases:
    (country, address) = get_country_and_address(as_number)
    output_good.write(f"{as_number}; {country}; {address} \n")

    bar.next()

bar.finish()


output_good.close()





