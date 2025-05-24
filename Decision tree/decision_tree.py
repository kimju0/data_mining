import sys
from collections import Counter
from math import log2

# if len(sys.argv) != 4:
#     print("Usage: python decision_tree.py <train_file> <test_file> <result_file>")
#     sys.exit(1)
TRAIN_FILE_NAME = "dt_train1.txt"  # sys.argv[1]
TEST_FILE_NAME = "dt_test1.txt"  # sys.argv[2]
RESULT_FILE_NAME = "dt_answer10.txt"  # sys.argv[3]


class Node:
    def __init__(self, attribute=None, label=None, depth=0):
        self.attribute = attribute
        self.label = label
        self.children = {}
        self.depth = depth

    def is_leaf(self):
        return self.label is not None


class DecisionTree:
    def __init__(self, data, attributes):
        self.root = self.build_tree(data, attributes)

    def build_tree(self, data, attributes):
        if not data:
            return None

        # Check if all samples have the same label
        labels = [row[-1] for row in data]
        if len(set(labels)) == 1:
            return Node(label=labels[0])

        # If no attributes left, return the most common label
        if not attributes:
            most_common_label = Counter(labels).most_common(1)[0][0]
            return Node(label=most_common_label)

        # Find the best attribute to split on
        gains = [gain_ratio(data, i) for i in range(len(attributes))]
        best_attribute_index = gains.index(max(gains))

        # Create a new node for the best attribute
        node = Node(attribute=best_attribute_index)

        # Split the data based on the best attribute
        attribute_values = set(row[best_attribute_index] for row in data)
        for value in attribute_values:
            subset = [row for row in data if row[best_attribute_index] == value]
            new_attributes = attributes[:best_attribute_index] + attributes[best_attribute_index + 1:]
            child_node = self.build_tree(subset, new_attributes)
            node.children[value] = child_node

        return node

    def classify(self, sample):
        current_node = self.root
        while not current_node.is_leaf():
            attribute_value = sample[current_node.attribute]
            current_node = current_node.children.get(attribute_value)
            if current_node is None:
                return None  # If no child exists for this attribute value
        return current_node.label


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
