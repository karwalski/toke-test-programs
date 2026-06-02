import heapq

def prim_mst():
    # Read input
    v, e = map(int, input().split())
    
    # Build adjacency list
    graph = [[] for _ in range(v)]
    for _ in range(e):
        u, node_v, w = map(int, input().split())
        graph[u].append((node_v, w))
        graph[node_v].append((u, w))
    
    start = int(input())
    
    # Prim's algorithm
    visited = [False] * v
    min_heap = [(0, start, -1)]  # (weight, node, parent)
    mst_edges = []
    total_weight = 0
    
    while min_heap:
        weight, u, parent = heapq.heappop(min_heap)
        
        if visited[u]:
            continue
            
        visited[u] = True
        
        if parent != -1:
            mst_edges.append((parent, u, weight))
            total_weight += weight
        
        # Add all adjacent edges to the priority queue
        for neighbor, edge_weight in graph[u]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (edge_weight, neighbor, u))
    
    # Output
    print("MST edges:", end="")
    for i, (u, v, w) in enumerate(mst_edges):
        print(f" {u}-{v} {w}")
    print(f"Total weight: {total_weight}")

prim_mst()