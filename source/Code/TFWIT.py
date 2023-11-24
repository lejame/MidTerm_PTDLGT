import time
from typing import List, Tuple, Set

def generate_candidates(frequent_itemsets: List[Set[int]], k: int) -> List[Set[int]]:
    candidates = []
    for i in range(len(frequent_itemsets)):
        for j in range(i + 1, len(frequent_itemsets)):
            itemset1 = frequent_itemsets[i]
            itemset2 = frequent_itemsets[j]
            candidate = itemset1.union(itemset2)
            if len(candidate) == k:
                candidates.append(candidate)
    return candidates

def calculate_support(dataset: List[List[Tuple[int, float]]], itemset: Set[int]) -> int:
    support = 0
    for tidset in dataset:
        if itemset.issubset(set(item for item, _ in tidset)):
            support += 1
    return support

def calculate_weight_support(dataset: List[List[Tuple[int, float]]], itemset: Set[int]) -> float:
    weight_support = 0
    for tidset in dataset:
        if itemset.issubset(set(item for item, _ in tidset)):
            for item, weight in tidset:
                if item in itemset:
                    weight_support += weight
                    break
    return weight_support

def tfwit(dataset: List[List[Tuple[int, float]]], min_support: int, k: int) -> List[Tuple[Set[int], float]]:
    frequent_itemsets = []
    weight_supports = []

    # Generate 1-itemsets
    itemsets = set()
    for tidset in dataset:
        for item, _ in tidset:
            itemsets.add(frozenset([item]))

    # Prune itemsets with minimum support
    frequent_1_itemsets = [itemset for itemset in itemsets if calculate_support(dataset, itemset) >= min_support]
    frequent_itemsets.extend(frequent_1_itemsets)

    # Calculate weight support for 1-itemsets
    for itemset in frequent_1_itemsets:
        weight_support = calculate_weight_support(dataset, itemset)
        weight_supports.append((itemset, weight_support))

    k_value = 2
    while frequent_itemsets:
        candidates = generate_candidates(frequent_itemsets, k_value)

        # Calculate support for candidates
        frequent_itemsets.clear()
        for candidate in candidates:
            support = calculate_support(dataset, candidate)
            if support >= min_support:
                frequent_itemsets.append(candidate)

        # Calculate weight support for candidates
        weight_supports.extend([(itemset, calculate_weight_support(dataset, itemset)) for itemset in frequent_itemsets])

        k_value += 1

    return weight_supports

# Example usage
dataset = [
    [(1, 0.5), (2, 0.3), (3, 0.2)],
    [(2, 0.4), (3, 0.1)],
    [(1, 0.6), (2, 0.2), (3, 0.4)],
    [(1, 0.3), (2, 0.5), (3, 0.3)],
    [(2, 0.1), (3, 0.7)]
]

min_support = 2
k = 4

start_time = time.time()
result = tfwit(dataset, min_support, k)
end_time = time.time()

runtime = end_time - start_time
print("Runtime: {:.9f} seconds".format(runtime))
print(result)