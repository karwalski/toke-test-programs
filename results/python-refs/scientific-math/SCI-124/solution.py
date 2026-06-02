from collections import defaultdict, deque

def bfs(graph, source, sink, parent):
    visited = set([source])
    queue = deque([source])
    
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

def ford_fulkerson(graph, source, sink):
    parent = {}
    max_flow = 0
    
    while bfs(graph, source, sink, parent):
        path_flow = float('inf')
        s = sink
        
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        
        max_flow += path_flow
        v = sink
        
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
        
        parent = {}
    
    return max_flow

def find_min_cut(original_graph, residual_graph, source, sink):
    visited = set()
    queue = deque([source])
    visited.add(source)
    
    while queue:
        u = queue.popleft()
        for v in residual_graph[u]:
            if v not in visited and residual_graph[u][v] > 0:
                visited.add(v)
                queue.append(v)
    
    cut_edges = []
    cut_value = 0
    
    for u in visited:
        for v in original_graph[u]:
            if v not in visited and original_graph[u][v] > 0:
                cut_edges.append((u, v, original_graph[u][v]))
                cut_value += original_graph[u][v]
    
    return cut_value, cut_edges

# Read input
line = input().split()
V, E = int(line[0]), int(line[1])

# Initialize graphs
original_graph = defaultdict(lambda: defaultdict(int))
residual_graph = defaultdict(lambda: defaultdict(int))

# Read edges
for _ in range(E):
    u, v, capacity = map(int, input().split())
    original_graph[u][v] = capacity
    residual_graph[u][v] = capacity

source = int(input())
sink = int(input())

# Find max flow
max_flow = ford_fulkerson(residual_graph, source, sink)

# Find min cut
cut_value, cut_edges = find_min_cut(original_graph, residual_graph, source, sink)

# Output
print(f"Min cut value: {cut_value}")
print("Cut edges:", end="")
for u, v, capacity in cut_edges:
    print(f" {u}->{v} {capacity}")