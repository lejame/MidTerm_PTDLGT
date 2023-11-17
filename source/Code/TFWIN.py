import time

# Cài đặt cấu trúc dữ liệu WN-list
class WNList:
    def __init__(self, pre, post, weight):
        self.pre = pre
        self.post = post
        self.weight = weight

# Tạo WN-list cho các item 1
def create_item_wnlists(items, weights, transactions):
    wnlists = {}

    for item in items:
        wnlist = []
        for t in transactions:
            if item in t:
                wnlist.append(WNList(t.index(item), len(t) - t.index(item), weights[item]))

        wnlists[item] = wnlist

    return wnlists

# Tìm giao của 2 WN-list
def intersect_wnlists(wnlist1, wnlist2):
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

# Tính ws cho một pattern dựa trên WN-list
def calc_ws(wnlist, total_weight):
    sum_weight = 0

    for node in wnlist:
        sum_weight += node.weight

    return sum_weight / total_weight

# Thuật toán chính
def tfwin(transactions, weights, k):
    items = list(set().union(*transactions))

    wnlists = create_item_wnlists(items, weights, transactions)

    topk = []

    # B1: Thêm các item 1 vào topk
    for item, wnlist in wnlists.items():
        ws = calc_ws(wnlist, sum(weights.values()))
        topk.append((item, ws))

    topk.sort(key=lambda x: x[1], reverse=True)
    topk = topk[:k]

    # B2: Tổ hợp và thêm vào topk
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

# Dữ liệu mẫu
dataset = [
    [(1, 0.5), (2, 0.8), (3, 0.3)],
    [(2, 0.6), (4, 0.7)],
    [(1, 0.4), (3, 0.2), (4, 0.9)],
    [(2, 0.7), (3, 0.5), (4, 0.3)],
    [(1, 0.2), (2, 0.4), (3, 0.6)],
    [(1, 0.3), (3, 0.5)],
    [(2, 0.9), (3, 0.3), (4, 0.7)],
]

# Chuyển đổi dataset thành dạng transactions
transactions = []
for transaction in dataset:
    t = []
    for item, weight in transaction:
        t.append(str(item))

    transactions.append(t)

# Khởi tạo weights
weights = {}
for transaction in dataset:
    for item, weight in transaction:
        weights[str(item)] = weight

# Chạy thuật toán
k = 3
result = tfwin(transactions, weights, k)

# In kết quả
print("Top-{} FWIs: ".format(k))
for x in result:
    print(x)

start = time.time()
result = tfwin(transactions, weights, k)
end = time.time()

running_time = end - start

print("Running time: ", running_time, "seconds")
