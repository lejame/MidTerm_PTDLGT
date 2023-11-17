import time

class TFWIT:
    def __init__(self, min_support):
        self.min_support = min_support
        self.itemsets = {}
    
    def add_transaction(self, transaction):
        for item, weight in transaction:
            if item in self.itemsets:
                self.itemsets[item] += weight
            else:
                self.itemsets[item] = weight
    
    def generate_itemsets(self):
        frequent_itemsets = []
        for item, support in self.itemsets.items():
            if support >= self.min_support:
                frequent_itemsets.append(([item], support))
        frequent_itemsets.sort(key=lambda x: x[1], reverse=True)
        return frequent_itemsets
    
    def get_top_k_itemsets(self, k):
        frequent_itemsets = self.generate_itemsets()
        return frequent_itemsets[:k]

# Example usage and benchmark
dataset = [
    [(1, 0.5), (2, 0.8), (3, 0.3)],
    [(2, 0.6), (4, 0.7)],
    [(1, 0.4), (3, 0.2), (4, 0.9)],
    [(2, 0.7), (3, 0.5), (4, 0.3)],
    [(1, 0.2), (2, 0.4), (3, 0.6)],
    [(1, 0.3), (3, 0.5)],
    [(2, 0.9), (3, 0.3), (4, 0.7)],
]

min_support = 2.0
k = 4

tfwit = TFWIT(min_support)

start_time = time.time()

for transaction in dataset:
    tfwit.add_transaction(transaction)

top_k_itemsets = tfwit.get_top_k_itemsets(k)

end_time = time.time()
running_time = end_time - start_time

print("Running time:", running_time, "seconds")

# Output top-k itemsets
for i, (itemset, support) in enumerate(top_k_itemsets):
    print("Rank {}: Itemset: {}, Weighted Support (ws): {}".format(i+1, itemset, support))