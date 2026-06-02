from collections import deque

# Read input
V, E = map(int, input().split())

# Build adjacency list
graph = [[] for _ in range(V)]
for _ in range(E):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

start = int(input())

# BFS
queue = deque([start])
visited = [False] * V
distances = [-1] * V
visit_order = []

visited[start] = True
distances[start] = 0
visit_order.append(start)

while queue:
    node = queue.popleft()
    
    for neighbor in graph[node]:
        if not visited[neighbor]:
            visited[neighbor] = True
            distances[neighbor] = distances[node] + 1
            visit_order.append(neighbor)
            queue.append(neighbor)

# Output
print("Visit order:", " ".join(map(str, visit_order)))
print("Distances:")
for i in range(V):
    if distances[i] != -1:
        print(f"{i}={distances[i]}")