# temporal const variable
INPUT_FILE_NAME = "input.txt"
OUTPUT_FILE_NAME = "output.txt"
MIN_SUPPORT = 5


# read the input file and parse the data
def read_input_file():
    datas = []
    with open(INPUT_FILE_NAME, 'r') as file:
        for line in file:
            datas.append(list(map(int, line.strip().split())))
    return datas


def apriori(datas, min_support):
    table = []
    candidates = {}
    for data in datas:
        for item in data:
            if item not in candidates:
                candidates[item] = 0
            candidates[item] += 1
    candidates = {k: v for k, v in candidates.items() if v >= min_support}
    table.append(candidates)
    if len(candidates) == 0:
        return table
    # 이어서 작성하기...
