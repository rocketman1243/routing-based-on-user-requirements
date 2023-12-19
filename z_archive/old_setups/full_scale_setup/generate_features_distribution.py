import random, math
import networkx as nx


def generate_distribution(max_number_of_features: int, min_nr_of_features: int, as_numbers: list[str], G):
    items_per_step = math.ceil(len(as_numbers) / (max_number_of_features - min_nr_of_features))



    distribution = {}

    counter = 0
    current_number_of_elements = max_number_of_features - min_nr_of_features

    for i in as_numbers:
        distribution[i] = current_number_of_elements + min_nr_of_features
        counter += 1

        if counter >= items_per_step:
            counter = 0
            current_number_of_elements -= 1

    return distribution


# Create method that generates a mapping of privacy and security features to a list of indexes
# distributed linearly decreasing over the list of indexes, ranging from 1-30 features per category
# per AS, such that lower index support higher numbers of features and higher indexes support lower number of features
def generate_features(max_number_of_features: int, min_nr_of_features: int, as_numbers: list[int], G):
    # Changed to allow programming for the max Best effort problem
    features = range(1, max_number_of_features + 1)
    distribution = generate_distribution(max_number_of_features, min_nr_of_features, as_numbers)

    mapping = {}

    degrees = list(nx.degree(G))
    degrees.sort(key=lambda x: x[1])
    degrees.reverse()

    ordered_asns = []
    for l in degrees:
        ordered_asns.append(l[0])

    for as_number in ordered_asns:
        nr_of_items = distribution[str(as_number)]
        sample = random.sample(features, nr_of_items)
        sample.sort()
        mapping[as_number] = sample

    return mapping

print(generate_distribution(5, 4, [1, 2, 3, 4, 5, 6], nx.path_graph(6)))