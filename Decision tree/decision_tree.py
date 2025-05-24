import sys
from collections import Counter
from math import log2

# if len(sys.argv) != 4:
#     print("Usage: python decision_tree.py <train_file> <test_file> <result_file>")
#     sys.exit(1)
TRAIN_FILE_NAME = "dt_train1.txt"  # sys.argv[1]
TEST_FILE_NAME = "dt_test1.txt"  # sys.argv[2]
RESULT_FILE_NAME = "dt_answer10.txt"  # sys.argv[3]


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    data = [line.strip().split() for line in lines]
    return data


def write_data(file_name, data):
    with open(file_name, 'w') as file:
        for line in data:
            file.write(' '.join(line) + '\n')


# format of data: [sample1, sample2, ..., sampleN]
# format of sample: [attribute1, attribute2, ..., attributeN, label]
def entropy(data):
    total_count = len(data)
    if total_count == 0:
        return 0

    label_counts = Counter(row[-1] for row in data)
    entropy_value = 0.0

    for count in label_counts.values():
        probability = count / total_count
        entropy_value -= probability * log2(probability)

    return entropy_value


def gain_ratio(data, attribute_index):
    total_entropy = entropy(data)
    total_count = len(data)

    if total_count == 0:
        return 0

    attribute_values = {}
    for row in data:
        value = row[attribute_index]
        if value not in attribute_values:
            attribute_values[value] = []
        attribute_values[value].append(row)

    weighted_entropy = 0.0
    split_info = 0.0

    for subset in attribute_values.values():
        subset_entropy = entropy(subset)
        probability = len(subset) / total_count
        weighted_entropy += probability * subset_entropy
        split_info -= probability * log2(probability)

    if split_info == 0:
        return 0

    return (total_entropy - weighted_entropy) / split_info


train_data = read_data(TRAIN_FILE_NAME)
attribute, train_data = train_data[0], train_data[1:]
test_data = read_data(TEST_FILE_NAME)[1:]
