from collections import defaultdict, deque

# Read input
V, E = map(int, input().split())

# Initialize graph and in-degree array
graph = defaultdict(list)
in_degree = [0] * V

# Build graph and calculate in-degrees
for _ in range(E):
    u, v = map(int, input().split())
    graph[u].append(v)
    in_degree[v] += 1

# Kahn's algorithm
queue = deque()
result = []

# Add all vertices with in-degree 0 to queue
for i in range(V):
    if in_degree[i] == 0:
        queue.append(i)

# Process vertices
while queue:
    vertex = queue.popleft()
    result.append(vertex)
    
    # Reduce in-degree of adjacent vertices
    for neighbor in graph[vertex]:
        in_degree[neighbor] -= 1
        if in_degree[neighbor] == 0:
            queue.append(neighbor)

# Check if all vertices were processed (no cycle)
if len(result) == V:
    print("Topological order:", " ".join(map(str, result)))
else:
    print("CYCLE")