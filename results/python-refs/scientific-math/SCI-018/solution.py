import sys

def bellman_ford(V, edges, source):
    # Initialize distances
    dist = [float('inf')] * V
    dist[source] = 0
    
    # Relax edges V-1 times
    for _ in range(V - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    
    # Check for negative weight cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # Negative cycle detected
    
    return dist

# Read input
line = input().split()
V, E = int(line[0]), int(line[1])

edges = []
for _ in range(E):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))

source = int(input())

# Solve
result = bellman_ford(V, edges, source)

# Output
if result is None:
    print("NEGATIVE CYCLE")
else:
    for i in range(V):
        if result[i] == float('inf'):
            print(f"{i}: INF")
        else:
            print(f"{i}: {result[i]}")