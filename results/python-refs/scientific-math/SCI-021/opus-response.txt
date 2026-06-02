import heapq

def prim_mst():
    v, e = map(int, input().split())
    
    graph = [[] for _ in range(v)]
    for _ in range(e):
        u, node_v, w = map(int, input().split())
        graph[u].append((node_v, w))
        graph[node_v].append((u, w))
    
    start = int(input())
    
    visited = [False] * v
    min_heap = [(0, start, -1)]
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
        
        for neighbor, edge_weight in graph[u]:
            if not visited[neighbor]:
                heapq.heappush(min_heap, (edge_weight, neighbor, u))
    
    lines = ["MST edges: " + f"{mst_edges[0][0]}-{mst_edges[0][1]} {mst_edges[0][2]}"] if mst_edges else ["MST edges:"]
    for i in range(1, len(mst_edges)):
        u, vv, w = mst_edges[i]
        lines.append(f"{u}-{vv} {w}")
    lines.append(f"Total weight: {total_weight}")
    print("\n".join(lines))

prim_mst()