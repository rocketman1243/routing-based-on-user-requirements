import random, math


def generate_distribution(max_number_of_features: int, as_numbers: list[int]) -> list[int]:
    items_per_step = math.ceil(len(as_numbers) / max_number_of_features)

    max_as = max(as_numbers)
    distribution = [0] * (max_as + 1)

    counter = 0
    current_number_of_elements = max_number_of_features

    for i in as_numbers:
        distribution[i] =  current_number_of_elements
        counter += 1

        if counter >= items_per_step:
            counter = 0
            current_number_of_elements -= 1

    return distribution


# Create method that generates a mapping of privacy and security features to a list of indexes 
# distributed linearly decreasing over the list of indexes, ranging from 1-30 features per category 
# per AS, such that lower index support higher numbers of features and higher indexes support lower number of features
def generate_features(max_number_of_features: int, as_numbers: list[int]) -> list[int]:
    features = range(1, max_number_of_features + 1)
    distribution = generate_distribution(max_number_of_features, as_numbers)


    # Generate list to hold as_number-to-features mapping
    max_as = max(as_numbers)
    mapping = [[]] * (max_as + 1)

    for as_number in as_numbers:
        nr_of_items = distribution[as_number]
        sample = random.sample(features, nr_of_items)
        sample.sort()
        mapping[as_number] = sample

    return mapping
