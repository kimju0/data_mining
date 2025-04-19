# temporal const variable
from itertools import combinations
import sys

if len(sys.argv) != 3:
    print("Usage: python main.py <input_file> <output_file>")
    sys.exit(1)
INPUT_FILE_NAME = sys.argv[1]
OUTPUT_FILE_NAME = sys.argv[2]
MIN_SUPPORT = 15


# return format: [(7, 14), (9), ...]
def read_input_file():
    datas = []
    with open(INPUT_FILE_NAME, 'r') as file:
        for line in file:
            data = sorted(list(map(int, line.strip().split())))
            datas.append(tuple(data))
    return datas, len(datas)


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
def make_association_rules(datas, N):
    table = []
    for frequent_itemset in datas:
        for itemset in frequent_itemset:
            for r in range(1, len(itemset)):
                for subset in combinations(itemset, r):
                    subset = tuple(sorted(subset))
                    remaining_items = tuple(sorted(set(itemset) - set(subset)))
                    support = frequent_itemset[itemset] / N
                    confidence = frequent_itemset[itemset] / datas[len(subset) - 1][subset]
                    table.append({
                        'association_rule': (subset, remaining_items),
                        'support': support,
                        'confidence': confidence
                    })

    return table


def format_table(table):
    formatted_table = []
    for item in table:
        A, B = item['association_rule']
        sup = item['support'] * 100
        conf = item['confidence'] * 100
        rule = f"{{{', '.join(map(str, A))}}}\t{{{', '.join(map(str, B))}}}\t{sup:.2f}\t{conf:.2f}\n"
        formatted_table.append(rule)
    return formatted_table


# make and write the output file
def write_output_file(formatted_res):
    with open(OUTPUT_FILE_NAME, 'w') as file:
        for item in formatted_res:
            file.write(item)


datas, N = read_input_file()
tables = apriori(datas, MIN_SUPPORT)
association_results = make_association_rules(apriori(datas, MIN_SUPPORT), N)
formatted_res = format_table(association_results)
write_output_file(formatted_res)
print("Output file written successfully.")
