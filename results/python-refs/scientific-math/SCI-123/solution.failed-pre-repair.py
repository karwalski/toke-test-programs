from collections import deque, defaultdict

def bfs_find_path(graph, source, sink, parent):
    visited = set()
    queue = deque([source])
    visited.add(source)
    
    while queue:
        u = queue.popleft()
        
        for v in graph[u]:
            if v not in visited and graph[u][v] > 0:
                visited.add(v)
                parent[v] = u
                if v == sink:
                    return True
                queue.append(v)
    
    return False

def ford_fulkerson(capacity, source, sink, V):
    # Create residual graph
    graph = defaultdict(lambda: defaultdict(int))
    
    # Build residual graph from capacity matrix
    for u in range(V):
        for v in range(V):
            if capacity[u][v] > 0:
                graph[u][v] = capacity[u][v]
    
    parent = [-1] * V
    max_flow = 0
    
    # Keep finding augmenting paths using BFS
    while bfs_find_path(graph, source, sink, parent):
        # Find minimum residual capacity along the path
        path_flow = float('inf')
        s = sink
        
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        
        # Add path flow to overall flow
        max_flow += path_flow
        
        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
    
    return max_flow, graph

# Read input
V, E = map(int, input().split())

# Initialize capacity matrix
capacity = [[0] * V for _ in range(V)]
edges = []

# Read edges
for _ in range(E):
    u, v, cap = map(int, input().split())
    capacity[u][v] = cap
    edges.append((u, v, cap))

source = int(input())
sink = int(input())

# Find maximum flow
max_flow, residual_graph = ford_fulkerson(capacity, source, sink, V)

print(f"Max flow: {max_flow}")
print("Flow on edges:", end="")

# Calculate flow on each edge
for u, v, cap in edges:
    flow = cap - residual_graph[u][v]
    print(f" {u}->{v}: {flow}/{cap}", end="")

print()