import requests
import json
from api_key import get_bing_apy_key # This key is in a local file. To reproduce, make a free bing maps key at https://www.microsoft.com/en-us/maps/create-a-bing-maps-key and use that to convert address to lat/lon
import geocoder

test_as = 198711
url = "https://api.bgpview.io/asn/" # + AS number as int

response = json.loads(requests.get(url + str(test_as)).text)

country = response["data"]["country_code"]
address = response["data"]["owner_address"]

address_as_string = ""

for i, part in enumerate(address):
    address_as_string += part 
    if i < len(address) - 1:
        address_as_string += ", "

g = geocoder.bing(address_as_string, key=get_bing_apy_key())
results = g.json
lat = results['lat']
lon = results['lon']


print(country)
print(address)
print(address_as_string)
print(f"lat: {lat}, lon: {lon}")

print("bing goodies along with lat/lon:")
print(results)