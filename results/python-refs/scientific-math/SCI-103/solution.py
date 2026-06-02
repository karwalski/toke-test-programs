import sys

class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree_sum = [0] * (4 * self.n)
        self.tree_min = [0] * (4 * self.n)
        self.arr = arr[:]
        self.build(1, 0, self.n - 1)
    
    def build(self, node, start, end):
        if start == end:
            self.tree_sum[node] = self.arr[start]
            self.tree_min[node] = self.arr[start]
        else:
            mid = (start + end) // 2
            self.build(2 * node, start, mid)
            self.build(2 * node + 1, mid + 1, end)
            self.tree_sum[node] = self.tree_sum[2 * node] + self.tree_sum[2 * node + 1]
            self.tree_min[node] = min(self.tree_min[2 * node], self.tree_min[2 * node + 1])
    
    def update(self, node, start, end, idx, val):
        if start == end:
            self.arr[idx] = val
            self.tree_sum[node] = val
            self.tree_min[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self.update(2 * node, start, mid, idx, val)
            else:
                self.update(2 * node + 1, mid + 1, end, idx, val)
            self.tree_sum[node] = self.tree_sum[2 * node] + self.tree_sum[2 * node + 1]
            self.tree_min[node] = min(self.tree_min[2 * node], self.tree_min[2 * node + 1])
    
    def query_sum(self, node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            return self.tree_sum[node]
        mid = (start + end) // 2
        p1 = self.query_sum(2 * node, start, mid, l, r)
        p2 = self.query_sum(2 * node + 1, mid + 1, end, l, r)
        return p1 + p2
    
    def query_min(self, node, start, end, l, r):
        if r < start or end < l:
            return float('inf')
        if l <= start and end <= r:
            return self.tree_min[node]
        mid = (start + end) // 2
        p1 = self.query_min(2 * node, start, mid, l, r)
        p2 = self.query_min(2 * node + 1, mid + 1, end, l, r)
        return min(p1, p2)
    
    def update_point(self, idx, val):
        self.update(1, 0, self.n - 1, idx, val)
    
    def range_sum(self, l, r):
        return self.query_sum(1, 0, self.n - 1, l, r)
    
    def range_min(self, l, r):
        return self.query_min(1, 0, self.n - 1, l, r)

n = int(input())
arr = list(map(int, input().split()))
st = SegmentTree(arr)

for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    
    parts = line.split()
    if parts[0] == "QUERY_SUM":
        l, r = int(parts[1]), int(parts[2])
        print(st.range_sum(l, r))
    elif parts[0] == "QUERY_MIN":
        l, r = int(parts[1]), int(parts[2])
        print(st.range_min(l, r))
    elif parts[0] == "UPDATE":
        idx, val = int(parts[1]), int(parts[2])
        st.update_point(idx, val)