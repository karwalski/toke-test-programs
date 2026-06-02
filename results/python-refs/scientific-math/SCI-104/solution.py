class FenwickTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (self.n + 1)
        for i in range(self.n):
            self.update(i + 1, arr[i])
    
    def update(self, i, delta):
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    
    def prefix_sum(self, i):
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & (-i)
        return result
    
    def range_sum(self, l, r):
        return self.prefix_sum(r) - self.prefix_sum(l - 1)

n = int(input())
arr = list(map(int, input().split()))
ft = FenwickTree(arr)

import sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        break
    
    parts = line.split()
    if parts[0] == "UPDATE":
        i = int(parts[1])
        delta = int(parts[2])
        ft.update(i, delta)
    elif parts[0] == "PREFIX":
        i = int(parts[1])
        print(ft.prefix_sum(i))
    elif parts[0] == "RANGE":
        l = int(parts[1])
        r = int(parts[2])
        print(ft.range_sum(l, r))