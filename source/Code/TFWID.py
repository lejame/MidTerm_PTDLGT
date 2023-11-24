from typing import List, Tuple, Dict
import time
class TFWID:
    def __init__(self, min_support: float):
        self.min_support = min_support
        self.itemsets: Dict[int, float] = {}

    def check_same_equivalence(self, c_i: 'TFWID', c_j: 'TFWID') -> bool:
        if len(c_i.itemsets) == 1 and len(c_j.itemsets) == 1:
            return True
        else:
            i = 0
            j = 0
            flag = True
            while i < len(c_i.itemsets) - 1 and j < len(c_j.itemsets) - 1:
                if c_i.itemsets[i] != c_j.itemsets[j]:
                    flag = False
                    break
                i += 1
                j += 1
            return flag

    def diffset_combination(self, a: Dict[int, float], b: Dict[int, float], hash_tw_of_trans: Dict[int, float], sum_tw: float) -> Dict[int, float]:
        result: Dict[int, float] = {}
        for b_key, b_value in b.items():
            diff = True
            for a_key, a_value in a.items():
                if b_key == a_key:
                    diff = False
                    break
            if diff:
                result[b_key] = b_value
                sum_tw += hash_tw_of_trans[b_key]
        return result

    def add_transaction(self, transaction: List[Tuple[int, float]]) -> None:
        for item, weight in transaction:
            if item in self.itemsets:
                self.itemsets[item] += weight
            else:
                self.itemsets[item] = weight

    def generate_itemsets(self) -> List[Tuple[List[int], float]]:
        frequent_itemsets = []
        for item, support in self.itemsets.items():
            if self.min_support is not None and support >= self.min_support:
                frequent_itemsets.append(([item], support))
        frequent_itemsets.sort(key=lambda x: x[1], reverse=True)
        return frequent_itemsets

    def get_top_k_itemsets(self, k: int) -> List[Tuple[List[int], float]]:
        frequent_itemsets = self.generate_itemsets()
        return frequent_itemsets[:k]

def tfwid_candidate_generation(candidate_k: List[Tuple[List[int], float]], hash_tw_of_trans: Dict[int, float], ttw: float) -> List[TFWID]:
    candidate_next: List[TFWID] = []
    for i in range(len(candidate_k) - 1, 0, -1):
        c_i = candidate_k[i]
        for j in range(i - 1, -1, -1):
            c_j = candidate_k[j]
            c = TFWID(None)
            if c.check_same_equivalence(c_i, c_j):
                sum_tw = 0.0
                if len(c_i.itemsets) != 1 and len(c_j.itemsets) != 1:
                    c.itemsets = c.diffset_combination(c_i.itemsets, c_j.itemsets, hash_tw_of_trans, sum_tw)
                else:
                    c.itemsets = c.diffset_combination(c_j.itemsets, c_i.itemsets, hash_tw_of_trans, sum_tw)
                candidate_next.append(c)
    return candidate_next

def measure_running_time(benchmark_dataset: List[List[Tuple[int, float]]], hash_tw_of_trans: Dict[int, float], ttw: float) -> Tuple[float, List[TFWID]]:
    start_time: float = time.time()
    tfwid = TFWID(None)
    for transaction in benchmark_dataset:
        tfwid.add_transaction(transaction)
    candidate_k = tfwid.generate_itemsets()
    result = tfwid_candidate_generation(candidate_k, hash_tw_of_trans, ttw)
    end_time: float = time.time()
    running_time: float = end_time - start_time
    return running_time, result

benchmark_dataset: List[List[Tuple[int, float]]] = [
    [(1, 0.5), (2, 0.8), (3, 0.3)],
    [(2, 0.6), (4, 0.7)],
    [(1, 0.4), (3, 0.2), (4, 0.9)],
    [(2, 0.7), (3, 0.5), (4, 0.3)],
    [(1, 0.2), (2, 0.4), (3, 0.6)],
    [(1, 0.3), (3, 0.5)],
    [(2, 0.9), (3, 0.3), (4, 0.7)],
]

hash_tw_of_trans: Dict[int, float] = {
    1: 0.5,
    2: 0.8,
    3: 0.3,
    4: 0.7
}
ttw: float = 0.0

running_time, result = measure_running_time(benchmark_dataset, hash_tw_of_trans, ttw)

print("Running time:", running_time, "seconds")
for c in result:
    print(c.itemsets)
