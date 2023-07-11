import requests
import json
import urllib.parse
from geopy.geocoders import Nominatim


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

# TODO: Convert address into lat/lon
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

response = requests.get(url).json()
print(response[0]["lat"])
print(response[0]["lon"])

print(country)
print(address)
print(address_as_string)
# print(lat, lon)