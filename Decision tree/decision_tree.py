import sys

if len(sys.argv) != 4:
    print("Usage: python decision_tree.py <train_file> <test_file> <result_file>")
    sys.exit(1)
TRAIN_FILE_NAME = sys.argv[1]
TEST_FILE_NAME = sys.argv[2]
RESULT_FILE_NAME = sys.argv[3]

def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    data = [line.strip().split(',') for line in lines]
    return data

def decision_tree(train_data, test_data):
    return ["dummy_class" for _ in test_data]