import random


def create_random_bits(amount_of_bits):
    bits = []
    for _ in range(amount_of_bits):
        bits.append(random.randint(0, 1))
    return bits


def convert_list_items_to_str(input_list):
    return [str(i) for i in input_list]
