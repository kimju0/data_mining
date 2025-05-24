import sys

# if len(sys.argv) != 4:
#     print("Usage: python decision_tree.py <train_file> <test_file> <result_file>")
#     sys.exit(1)
TRAIN_FILE_NAME = "dt_train1.txt"  # sys.argv[1]
TEST_FILE_NAME = "dt_test1.txt"  # sys.argv[2]
RESULT_FILE_NAME = "dt_answer1.txt"  # sys.argv[3]


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    data = [line.strip().split() for line in lines]
    return data[0], data[1:]

def OneHot_encode(attribute):


def decision_tree(train_data, test_data):
    return ["dummy_class" for _ in test_data]


attribute, data = read_data(TRAIN_FILE_NAME)
print(data)
