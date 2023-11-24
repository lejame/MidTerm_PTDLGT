import time
from typing import List, Tuple, Dict

class WNList:
    def __init__(self, pre: int, post: int, weight: float):
        self.pre = pre
        self.post = post
        self.weight = weight

def create_item_wnlists(items: List[str], weights: Dict[str, float], transactions: List[List[str]]) -> Dict[str, List[WNList]]:
    wnlists = {}

    for item in items:
        wnlist = []
        for t in transactions:
            if item in t:
                wnlist.append(WNList(t.index(item), len(t) - t.index(item), weights[item]))

        wnlists[item] = wnlist

    return wnlists

def intersect_wnlists(wnlist1: List[WNList], wnlist2: List[WNList]) -> List[WNList]:
    i = 0
    j = 0

    intersect = []

    while i < len(wnlist1) and j < len(wnlist2):
        if wnlist1[i].pre <= wnlist2[j].pre and wnlist1[i].post >= wnlist2[j].post:
            intersect.append(WNList(wnlist1[i].pre, wnlist1[i].post, wnlist2[j].weight))
            j += 1
        else:
            i += 1

    return intersect

def calc_ws(wnlist: List[WNList], total_weight: float) -> float:
    sum_weight = 0

    for node in wnlist:
        sum_weight += node.weight

    return sum_weight / total_weight

def tfwin(transactions: List[List[str]], weights: Dict[str, float], k: int) -> List[Tuple[str, float]]:
    items = list(set().union(*transactions))

    wnlists = create_item_wnlists(items, weights, transactions)

    topk = []

    for item, wnlist in wnlists.items():
        ws = calc_ws(wnlist, sum(weights.values()))
        topk.append((item, ws))

    topk.sort(key=lambda x: x[1], reverse=True)
    topk = topk[:k]

    i = 0
    while i < len(topk):
        pivot = topk[i][0]
        for j in range(i + 1, len(topk)):
            item = topk[j][0]

            if len(pivot) < len(item):
                continue

            wnlist = intersect_wnlists(wnlists[pivot], wnlists[item])
            ws = calc_ws(wnlist, sum(weights.values()))

            if ws > topk[-1][1]:
                topk.append((pivot + item, ws))
                topk.sort(key=lambda x: x[1], reverse=True)
                topk = topk[:k]

        i += 1

    return topk

# Sample dataset
dataset: List[List[Tuple[str, float]]] = [
    [('1', 0.5), ('2', 0.8), ('3', 0.3)],
    [('2', 0.6), ('4', 0.7)],
    [('1', 0.4), ('3', 0.2), ('4', 0.9)],
    [('2', 0.7), ('3', 0.5), ('4', 0.3)],
    [('1', 0.2), ('2', 0.4), ('3', 0.6)],
    [('1', 0.3), ('3', 0.5)],
    [('2', 0.9), ('3', 0.3), ('4', 0.7)],
]

# Convert dataset to transactions
transactions = [[item[0] for item, _ in transaction] for transaction in dataset]

# Initialize weights
weights = {item: weight for transaction in dataset for item, weight in transaction}

# Run the algorithm and measure running time
k = 3
start_time = time.time()
result = tfwin(transactions, weights, k)
end_time = time.time()

# Print the result and running time
print("Top-{} FWIs: ".format(k))
for x in result:
    print(x)

running_time = end_time - start_time
print("Running time: {:.6f} seconds".format(running_time))
