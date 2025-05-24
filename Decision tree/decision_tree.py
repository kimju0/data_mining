import sys
from collections import Counter
from math import log2

# if len(sys.argv) != 4:
#     print("Usage: python decision_tree.py <train_file> <test_file> <result_file>")
#     sys.exit(1)
TRAIN_FILE_NAME = "dt_train1.txt"  # sys.argv[1]
TEST_FILE_NAME = "dt_test1.txt"  # sys.argv[2]
RESULT_FILE_NAME = "dt_answer10.txt"  # sys.argv[3]
ANSWER_FILE_NAME = "dt_answer1.txt"
MAX_DEPTH = 15


class Node:
    def __init__(self, attribute=None, label=None, depth=0):
        self.attribute = attribute
        self.label = label
        self.children = {}
        self.depth = depth

    def is_leaf(self):
        return self.label is not None


class DecisionTree:
    def __init__(self, data):
        self.root = self.build_tree(data, 0)

    def build_tree(self, data, depth):
        labels = [row[-1] for row in data]
        most_common_label = Counter(labels).most_common(1)[0][0]

        # 모두 같은 레이블인 경우 리프 노드 반환
        if len(set(labels)) == 1:
            return Node(label=labels[0], depth=depth)

        # 더이상 분할하지 못하면 리프 노드 반환
        if sum(attr_flag) == 0 or depth >= MAX_DEPTH:
            return Node(label=most_common_label, depth=depth)

        gains = [gain_ratio(data, i) for i in range(len(attribute))]
        best_attribute_index = gains.index(max(gains))

        node = Node(attribute=best_attribute_index, depth=depth)

        # data 분할
        for value in attr_values[best_attribute_index]:
            subset = [row for row in data if row[best_attribute_index] == value]
            if not subset or attr_flag[best_attribute_index] == 0:
                node.children[value] = Node(label=most_common_label, depth=depth + 1)
            else:
                attr_flag[best_attribute_index] = 0
                child_node = self.build_tree(subset, depth + 1)
                node.children[value] = child_node
                attr_flag[best_attribute_index] = 1

        return node

    def classify(self, sample):
        current_node = self.root
        while not current_node.is_leaf():
            attribute_value = sample[current_node.attribute]
            current_node = current_node.children.get(attribute_value)
            if current_node is None:
                return None
        return current_node.label

    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.root
        if node.is_leaf():
            print("\t" * depth + f"Leaf: {node.label} (depth {node.depth})")
        else:
            print("\t" * depth + f"Node: {node.attribute} (depth {node.depth})")
            for value, child in node.children.items():
                print("\t" * (depth + 1) + f"Value: {value}")
                self.print_tree(child, depth + 2)


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    data = [line.strip().split() for line in lines]
    return data


def write_data(file_name, data):
    with open(file_name, 'w') as file:
        for line in data:
            file.write('\t'.join(line) + '\n')


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
    if attr_flag[attribute_index] == 0:
        return 0
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


def print_accuracy():
    A = read_data(ANSWER_FILE_NAME)[1:]
    R = read_data(RESULT_FILE_NAME)
    correct_count = 0
    for i in range(len(A)):
        if A[i][-1] == R[i][-1]:
            correct_count += 1
    accuracy = correct_count / len(A) * 100
    print(f"Accuracy: {accuracy}")


train_data = read_data(TRAIN_FILE_NAME)
attribute, train_data = train_data[0][:-1], train_data[1:]
attr_flag = [1] * len(attribute)
test_data = read_data(TEST_FILE_NAME)[1:]
attr_values = [set(row[i] for row in train_data) for i in range(len(attribute))]

tree = DecisionTree(train_data)

predictions = [tree.classify(sample) for sample in test_data]
for i in range(len(test_data)):
    test_data[i].append(predictions[i])
tree.print_tree()
write_data(RESULT_FILE_NAME, test_data)

print_accuracy()
