# temporal const variable
from itertools import combinations

INPUT_FILE_NAME = "input.txt"
OUTPUT_FILE_NAME = "output.txt"
MIN_SUPPORT = 35


# return format: [(7, 14), (9), ...]
def read_input_file():
    datas = []
    with open(INPUT_FILE_NAME, 'r') as file:
        for line in file:
            data = sorted(list(map(int, line.strip().split())))
            datas.append(tuple(data))
    return datas


# table contains all of frequent itemsets, table = [1-frequent_itemset, 2-frequent_itemset, ...]
# each frequent_itemset contains the count of each itemset, x-frequent_itemset = {itemset1: count, itemset2: count, ...}
# each itemset is a list of items, (item1, item2, ...)
def apriori(datas, min_support):
    table = []
    cur_frequent_itemset = {}
    for data in datas:
        for item in data:
            if item not in cur_frequent_itemset:
                cur_frequent_itemset[item] = 0
            cur_frequent_itemset[item] += 1
    cur_frequent_itemset = {(k,): v for k, v in cur_frequent_itemset.items() if v >= min_support}

    while len(cur_frequent_itemset) > 0:
        table.append(cur_frequent_itemset)
        next_frequent_itemset = {}
        for i in range(len(cur_frequent_itemset)):
            for j in range(i + 1, len(cur_frequent_itemset)):
                # merge two itemsets
                itemset1 = list(cur_frequent_itemset.keys())[i]
                itemset2 = list(cur_frequent_itemset.keys())[j]
                merged_itemset = tuple(sorted(set(itemset1) | set(itemset2)))
                if len(merged_itemset) != len(itemset1) + 1:
                    continue
                is_frequent = True
                for k in range(len(merged_itemset)):
                    subset = tuple(sorted(set(merged_itemset) - {merged_itemset[k]}))
                    if subset not in cur_frequent_itemset:
                        is_frequent = False
                        break
                if not is_frequent:
                    continue
                # count the support of the merged itemset
                count = 0
                for data in datas:
                    if set(merged_itemset).issubset(set(data)):
                        count += 1
                if count >= min_support:
                    next_frequent_itemset[merged_itemset] = count
        cur_frequent_itemset = next_frequent_itemset

    return table


# table contains all association rules, table = [1-association_rule, 2-association_rule, ...]
# each association_rule contains the values of support, confidence, x-association_rule = {association_rule: (itemset1, itemset2), support: support, confidence: confidence}
# each association_rule is a tuple of itemsets, (itemset1, itemset2)
def make_association_rules(datas):
    table = []
    for frequent_itemset in datas:
        for itemset in frequent_itemset:
            # 여기서 부분 집합들 찾고 값 계산
            # 이 집합을 두 부분으로 나누기
            for r in range(len(frequent_itemset[itemset])):
                combinations(itemset, r)
                
# print(read_input_file())
# print(apriori(read_input_file(), MIN_SUPPORT))
print(make_association_rules(read_input_file()))
