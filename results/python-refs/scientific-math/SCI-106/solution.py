class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y:
            # union by rank
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1
            self.components -= 1
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

n = int(input())
uf = UnionFind(n)

while True:
    try:
        line = input().strip()
        if not line:
            break
        
        parts = line.split()
        command = parts[0]
        
        if command == "UNION":
            a, b = int(parts[1]), int(parts[2])
            uf.union(a, b)
        elif command == "FIND":
            a = int(parts[1])
            print(uf.find(a))
        elif command == "CONNECTED":
            a, b = int(parts[1]), int(parts[2])
            print("true" if uf.connected(a, b) else "false")
        elif command == "COMPONENTS":
            print(uf.components)
    except EOFError:
        break