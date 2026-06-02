class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True

# Read input
v, e = map(int, input().split())
edges = []
for _ in range(e):
    u, v_node, w = map(int, input().split())
    edges.append((w, u, v_node))

# Sort edges by weight
edges.sort()

# Kruskal's algorithm
uf = UnionFind(v)
mst_edges = []
total_weight = 0

for weight, u, v_node in edges:
    if uf.union(u, v_node):
        mst_edges.append((u, v_node, weight))
        total_weight += weight

# Sort MST edges by weight for output
mst_edges.sort(key=lambda x: x[2])

# Output
print("MST edges:", end="")
for u, v_node, weight in mst_edges:
    print(f" {u}-{v_node} {weight}")
print(f"Total weight: {total_weight}")