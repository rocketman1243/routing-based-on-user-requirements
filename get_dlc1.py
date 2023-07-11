import requests
import json
from api_key import get_bing_apy_key # This key is in a local file. To reproduce, make a free bing maps key at https://www.microsoft.com/en-us/maps/create-a-bing-maps-key and use that to convert address to lat/lon
import geocoder
from progress.bar import Bar
from dlc_1_input import get_dlc1_input


ases = get_dlc1_input()

country_address_file = open("asn_data/dlc_1_output_country_address.csv", "w")
country_address_file.write("as_number; country; address \n")
country_address_file.close()
country_address_file = open("asn_data/dlc_1_output_country_address.csv", "a")

dlc2_no_address_file = open("dlc_2_input_no_address.csv", "w")
dlc2_no_address_file.write("as_number, country \n")
dlc2_no_address_file.close()
dlc2_no_address_file = open("dlc_2_input_no_address.csv", "a")

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
            dlc2_no_address_file.write(f"{as_number}, {country} \n")




bar = Bar("addresses", max = len(ases))
for as_number in ases:
    (country, address) = get_country_and_address(as_number)
    country_address_file.write(f"{as_number}; {country}; {address} \n")

    bar.next()

bar.finish()


country_address_file.close()




