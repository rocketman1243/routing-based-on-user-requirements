import requests
import networkx as nx
import json
import matplotlib.pyplot as plt
from types import SimpleNamespace

AS = 3333
url = f"https://stat.ripe.net/data/bgp-state/data.json?resource=3333"
data = json.loads(requests.get(url).text)

paths = set()
for path in data["data"]["bgp_state"]:
    t = tuple(path["path"])
    paths.add(t)


print(len(paths))
for p in paths:
    print(p)
