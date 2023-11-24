from typing import List, Any
import time
class NodeCode:
    def __init__(self, post_order: Any, pre_order: Any, tw: float):
        self.post_order = post_order
        self.pre_order = pre_order
        self.tw = tw

class TR:
    def __init__(self):
        self.fwi_list: List[Any] = []
        self.ws: float = 0.0

class FWI:
    def __init__(self):
        self.n_cs: List[Any] = []
        self.ws: float = 0.0

def check_same_equivalence(c_i: FWI, c_j: FWI) -> bool:
    # Kiểm tra tính tương đương giữa c_i và c_j
    return False

def tfwinplus_candidate_generation(candidate_k: List[FWI], threshold: float, ttw: float) -> List[FWI]:
    candidate_next: List[FWI] = []
    for i in range(len(candidate_k) - 1, 0, -1):
        c_i = candidate_k[i]
        for j in range(i - 1, -1, -1):
            c_j = candidate_k[j]
            if check_same_equivalence(c_i, c_j):
                c = FWI()
                if c_i.ws < threshold or c_j.ws < threshold:
                    continue
                sum_tw = 0
                # Assume node_code_combination returns a List of NodeCode instances
                c.n_cs = node_code_combination(c_i.n_cs, c_j.n_cs)
                candidate_next.append(c)
    return candidate_next

def tfwinplus(benchmark_dataset: List[List[Any]], threshold: float, ttw: float) -> List[FWI]:
    fwis_1: List[FWI] = []

    num_of_trans: int = len(benchmark_dataset)
    sum_trans_length: int = sum(len(trans) for trans in benchmark_dataset)

    candidate_k: List[FWI] = []

    while candidate_k:
        candidate = tfwinplus_candidate_generation(candidate_k, threshold, ttw)
        candidate.sort(key=lambda x: x.ws, reverse=True)
        fwis_top_rank_k = [c for c in candidate if c.ws >= threshold]
        fwis_1.extend(fwis_top_rank_k)
        candidate_k = fwis_top_rank_k
    return fwis_1

benchmark_dataset: List[List[Any]] = [
    ['A', 'B', 'C'],
    ['A', 'B'],
    ['A', 'C', 'D'],
    ['B', 'C', 'D'],
    ['B', 'C'],
    ['A', 'C'],
    ['A', 'B'],
    ['C', 'D'],
    ['A', 'B', 'C', 'D']
]
threshold: float = 0.5
ttw: float = 0.2

def measure_running_time(benchmark_dataset: List[List[Any]], threshold: float, ttw: float) -> tuple[float, List[FWI]]:
    start_time: float = time.time()
    fwis = tfwinplus(benchmark_dataset, threshold, ttw)
    end_time: float = time.time()
    running_time: float = end_time - start_time
    return running_time, fwis

running_time, fwis = measure_running_time(benchmark_dataset, threshold, ttw)

print("Frequent Weighted Itemsets:")
for fwi in fwis:
    print(fwi.n_cs, fwi.ws)

print("Running time:", running_time, "seconds")
