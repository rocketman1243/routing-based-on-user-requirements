import requests
import networkx as nx
import json
from types import SimpleNamespace


asn_filename = "asn_data/asns.jsonl"
asn_file = open(asn_filename)
asn_content = asn_file.read()
asn_object = json.loads(asn_content, object_hook=lambda asn_content: SimpleNamespace(**asn_content))

links_filename = "asn_data/asnLinks.jsonl"
links_file = open(links_filename)
links_content = links_file.read()
links_object = json.loads(links_content, object_hook=lambda links_content: SimpleNamespace(**links_content))


for s in as_object:
    node = s.edges.node.asn
    nodes.add(node)

for l in links_object.edges:
    node1 = node.asn0.asn 
    node2 = node.asn1.asn
    edges.append([node1, node2])

nodes = []
edges = []

G = nx.Graph()

G.add_nodes_from(nodes)
G.add_edges_from(edges)

print(G.nodes)
print(G.edges)