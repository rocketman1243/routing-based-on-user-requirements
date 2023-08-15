from get_incomplete_nodes import get_nodes
import requests, json

ases = get_nodes()

file = open("dlc2_output.csv", "w")

for i, num in enumerate(ases):
    # url = "https://api.asrank.caida.org/v2/restful/asns/" + num
    # data = json.loads(requests.get(url).text)["data"]["asn"]
    # if data is None:
    #     continue

    country = "US"
    lat = 0
    lon = 0

    print(f"{i+1}/{len(ases)} - {num},{country},{lat},{lon}\n")

    file.write(f"{num},{country},{lat},{lon}\n")

file.close()