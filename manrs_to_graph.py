import json
from types import SimpleNamespace
import networkx as nx
import random

node_attributes = {}

with open("node_attributes.csv") as file:
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
with open("country_to_latlon.csv") as file:
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
with open("asn_info_caida.json") as caida_file:
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

with open("manrs.json") as manrs_file:
    manrs_content = manrs_file.read()
    manrs_object = json.loads(manrs_content, object_hook=lambda manrs_content: SimpleNamespace(**manrs_content))
    
    for participant in manrs_object.participants:

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

with open("as-links.txt") as file:
    for full_line in file:
        line = full_line.split("|")
        a = int(line[0])
        b = int(line[1])
        if a in participant_asns and b in participant_asns:
            links.append([a, b])

G.add_edges_from(links)


# Add random edges to connect graph:

# Add 1 edge connecting each subset to the next to make a connected graph
line_graph = []
for subset in sorted(nx.connected_components(G), key=len, reverse=True):
    line_graph.append(list(subset)[0])

for i in range(len(line_graph) - 1): 
    G.add_edge(line_graph[i], line_graph[i + 1])

# Add some random edges

# This amount of random edges gives an average degree of around 13.3, 
# which is similar to the average degree of the full-size graph with 75k nodes and 500k edges
nr_of_random_edges = 6750 
for i in range(nr_of_random_edges):
    edge = random.sample(participant_asns, 2)
    G.add_edge(edge[0], edge[1])


# total_degree = 0
# for node in G.nodes:
#     total_degree += nx.degree(G, node)
# average = total_degree / len(G.nodes)
# print(average, " average degree")


# Convert this graph to NIO objects
geolocation = nx.get_node_attributes(G, "geolocation")
lat = nx.get_node_attributes(G, "lat")
lon = nx.get_node_attributes(G, "lon")
filtering = nx.get_node_attributes(G, "filtering")
anti_spoofing = nx.get_node_attributes(G, "anti_spoofing")
coordination = nx.get_node_attributes(G, "coordination")
routing_information = nx.get_node_attributes(G, "routing_information")

for asn in participant_asns:

    edges = []
    for edge in nx.edges(G, asn):
        edges.append(edge[1])
    
    nio = {
        "as_number": asn,
        "geolocation": geolocation[asn],
        "lat": lat[asn],
        "lon": lon[asn],
        "connections": edges,
        "filtering": filtering[asn],
        "anti_spoofing": anti_spoofing[asn],
        "coordination": coordination[asn],
        "routing_information": routing_information[asn]
    }

    with open(f"manrs_nio_files/nio_{asn}.json", "w") as file:
        file.write(f"{json.dumps(nio, indent=2)}")






       