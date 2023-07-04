import random, math


def generate_distribution(max_number_of_features: int, nr_of_ases: int) -> list[int]:
    items_per_step = math.ceil(nr_of_ases / max_number_of_features)

    distribution = []
    counter = 0
    current_number_of_elements = items_per_step
    for i in range(nr_of_ases):
        distribution.append(current_number_of_elements)
        counter += 1

        if counter >= items_per_step:
            counter = 0
            current_number_of_elements -= 1






def generate_features(max_number_of_features: int, as_numbers: list[int]) -> list[int]:
    features = range(1, 31)
    mapping = []

    for index, ass in enumerate(as_numbers):
        sample = random.sample(features, )