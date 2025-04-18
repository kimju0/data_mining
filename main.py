# temporal const variable
from sqlite3.dbapi2 import apilevel

INPUT_FILE_NAME = "test.txt"
OUTPUT_FILE_NAME = "output.txt"
MIN_SUPPORT = 2


# return format: [(7, 14), (9), ...]
def read_input_file():
    datas = []
    with open(INPUT_FILE_NAME, 'r') as file:
        for line in file:
            data = sorted(list(map(int, line.strip().split())))
            datas.append(tuple(data))
    return datas


# 강의자료 수도코드
# DO: Scan DB once to get frequent 1-itemsets
# REPEAT
# (Candidate Generation) Generate length-(k+1) candidates from length-k frequent itemsets
# (Candidate test) Test the candidates against DB if they are frequent or not
# UNTIL: No more frequent candidate itemset can be generated
# RETURN: all the obtained frequent itemsets

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

print(read_input_file())
print(apriori(read_input_file(), MIN_SUPPORT))
