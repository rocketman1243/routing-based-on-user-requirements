import random, math


# def generate_distribution(number_of_features_per_as: int, as_numbers: list[str]):

#     distribution = {}

#     for i in as_numbers:
#         distribution[i] = number_of_features_per_as

#     return distribution


# Create method that generates a mapping of privacy and security features to a list of indexes 
# distributed linearly decreasing over the list of indexes, ranging from 1-30 features per category 
# per AS, such that lower index support higher numbers of features and higher indexes support lower number of features
def generate_features(number_of_features_per_as: int, as_numbers):
    # Changed to allow programming for the max Best effort problem
    features = list(range(1, number_of_features_per_as + 1))

    mapping = {}

    for as_number in as_numbers:
        mapping[as_number] = random.sample(features, random.randint(0, len(features)))

    return mapping

