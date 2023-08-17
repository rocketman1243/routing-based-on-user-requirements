import json
from types import SimpleNamespace
import networkx as nx
import random




experiment = "proof_of_concept_experiment"











########################



node_attributes = {}

with open("data/node_attributes.csv") as file:
    for full_line in file:
        line = full_line.split(",")
        asn = line[0]
        country = line[1]
        lat = line[2]
        lon = line[3][:-1]

        node_attributes[asn] = {
            "country": country,
            "lat": lat,
            "lon": lon
        }

country_to_latlon = {}
with open("data/country_to_latlon.csv") as file:
    for full_line in file:
        line = full_line.split(",")
        country = line[0][1:-1]
        lat = line[2]
        lon = line[3][:-1]

        country_to_latlon[country] = {
            "lat": lat,
            "lon": lon
        }


participant_asns = []

extra_node_info = {}
with open("data/asn_info_caida.json") as caida_file:
    caida_content = caida_file.read()
    caida_object = json.loads(caida_content, object_hook=lambda caida_content: SimpleNamespace(**caida_content))
    asns = caida_object.data.asns.edges

    for item in asns:
        network = item.node 
        asn = network.asn 
        country = network.country.iso
        lat = network.latitude
        lon = network.longitude

        if asn not in node_attributes:
            node_attributes[asn] = {
                "country": country,
                "lat": lat,
                "lon": lon
            }




node_features = {}

with open("data/manrs.json") as file:
    content = file.read()
    object = json.loads(content, object_hook=lambda content: SimpleNamespace(**content))
    
    for participant in object.participants:

        for asn in participant.ASNs:
            asn = str(asn)
            participant_asns.append(asn)

            lat = 0
            lon = 0
            geolocation = participant.areas_served


            if asn in node_attributes:
                # Set lat and lon for the AS for latency estimation
                lat = node_attributes[asn]["lat"]
                lon = node_attributes[asn]["lon"]

                # Add country to the list of geolocations if not alreasy in there
                country = node_attributes[asn]["country"]
                if country not in geolocation:
                    geolocation.append(country)
            else:
                country = geolocation[0]
                lat = country_to_latlon[str(country)]["lat"]
                lon = country_to_latlon[str(country)]["lon"]

            features = {
                "geolocation": geolocation,
                "lat": lat,
                "lon": lon,

                # One of ["conformant", "nonconformant"])
                "filtering": participant.filtering.conformance, 
                "anti_spoofing": participant.anti_spoofing.conformance, 
                "coordination": participant.coordination.conformance, 
                "routing_information": participant.routing_information.conformance, 
            }

            node_features[asn] = features

# Remove duplicate asns
participant_asns = list(set(participant_asns))

G = nx.Graph()
G.add_nodes_from(participant_asns)
nx.set_node_attributes(G, node_features)


# TODO: Make graph connected
 
# 1. Add the real links from as-links.txt for which both endpoints are present in the graph
links = []

with open("data/as-links.txt") as file:
    for full_line in file:
        line = full_line.split("|")
        a = line[0]
        b = line[1]
        if a in participant_asns and b in participant_asns:
            links.append([a, b])

G.add_edges_from(links)



# Add 1 edge connecting each subset to the next to make a connected graph
line_graph = []
for subset in sorted(nx.connected_components(G), key=len, reverse=True):
    line_graph.append(list(subset)[0])

for i in range(len(line_graph) - 1): 
    G.add_edge(line_graph[i], line_graph[i + 1])

total_degree = 0
for node in G.nodes:
    total_degree += nx.degree(G, node)
average = total_degree / len(G.nodes)
print(average, " average degree")
print("#connected components:", nx.number_connected_components(G))

print(len(G.edges), " edges")
print(len(G.nodes), " nodes")



# Convert this graph to NIO objects
geolocation = nx.get_node_attributes(G, "geolocation")
lat = nx.get_node_attributes(G, "lat")
lon = nx.get_node_attributes(G, "lon")


for asn in participant_asns:
    features = []
    if nx.get_node_attributes(G, "filtering")[asn] == "conformant":
        features.append("filtering")
    if nx.get_node_attributes(G, "anti_spoofing")[asn] == "conformant":
        features.append("anti_spoofing")
    if nx.get_node_attributes(G, "coordination")[asn] == "conformant":
        features.append("coordination")
    if nx.get_node_attributes(G, "routing_information")[asn] == "conformant":
        features.append("routing_information")

    edges = []
    for edge in nx.edges(G, asn):
        edges.append(edge[1])
    
    nio = {
        "as_number": asn,
        "geolocation": geolocation[asn],
        "lat": lat[asn],
        "lon": lon[asn],
        "connections": edges,
        "features": features
    }

    # Commented for now so I can easily re-run this script for statistics.
    # Uncomment to re-generate the NIO files

    # with open(f"{experiment}/nio_files/nio_{asn}.json", "w") as file:
    #     file.write(f"{json.dumps(nio, indent=2)}")






       