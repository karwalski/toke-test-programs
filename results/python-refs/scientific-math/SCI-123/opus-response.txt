The bug: when reading edges, if there's a reverse edge already (like `2 1 4` after `1 2 10`), setting capacity[u][v] overwrites. But actually the issue is the residual graph initialization — when building, we set graph[u][v] = capacity[u][v], but for reverse edges in input both exist. Actually the real bug: BFS uses `graph[u]` which is a defaultdict — iterating creates issues? No.

Actually issue: in test 1, edges `1 2 10` and `2 1 4` are both forward edges. The residual init does graph[1][2]=10 and graph[2][1]=4. That's fine. But during augmentation, we add reverse flow: graph[v][u] += path_flow, which adds to graph[2][1] for example, mixing it with the actual edge capacity 4.

This is the classic problem with parallel/antiparallel edges. Need to track them separately.

```python
from collections import deque

def solve():
    import sys
    data = sys.stdin.read().split()
    idx = 0
    V = int(data[idx]); idx+=1
    E = int(data[idx]); idx+=1
    
    edges = []  # (u, v, cap)
    # For each edge, we create forward edge with capacity, and backward with 0
    # Use edge list representation
    graph = [[] for _ in range(V)]  # adjacency list of edge indices
    edge_to = []  # destination
    edge_cap = []  # remaining capacity
    edge_orig_cap = []
    
    for _ in range(E):
        u = int(data[idx]); idx+=1
        v = int(data[idx]); idx+=1
        c = int(data[idx]); idx+=1
        edges.append((u, v, c))
        # forward edge
        graph[u].append(len(edge_to))
        edge_to.append(v)
        edge_cap.append(c)
        edge_orig_cap.append(c)
        # backward edge
        graph[v].append(len(edge_to))
        edge_to.append(u)
        edge_cap.append(0)
        edge_orig_cap.append(0)
    
    source = int(data[idx]); idx+=1
    sink = int(data[idx]); idx+=1
    
    # We need to remember which edge index corresponds to each input edge
    edge_indices = [i*2 for i in range(E)]
    
    max_flow = 0
    while True:
        # BFS
        parent_edge = [-1]*V
        parent_node = [-1]*V
        visited = [False]*V
        visited[source] = True
        q = deque([source])
        while q and not visited[sink]:
            u = q.popleft()
            for ei in graph[u]:
                v = edge_to[ei]
                if not visited[v] and edge_cap[ei] > 0:
                    visited[v] = True
                    parent_edge[v] = ei
                    parent_node[v] = u
                    q.append(v)
        if not visited[sink]:
            break
        # find bottleneck
        path_flow = float('inf')
        v = sink
        while v != source:
            ei = parent_edge[v]
            path_flow = min(path_flow, edge_cap[ei])
            v = parent_node[v]
        # update
        v = sink
        while v != source:
            ei = parent_edge[v]
            edge_cap[ei] -= path_flow
            edge_cap[ei ^ 1] += path_flow
            v = parent_node[v]
        max_flow += path_flow
    
    print(f"Max flow: {max_flow}")
    parts = ["Flow on edges:"]
    for i, (u, v, c) in enumerate(edges):
        ei = edge_indices[i]
        flow = c - edge_cap[ei]
        parts.append(f" {u}->{v}: {flow}/{c}")
    print("".join(parts))

solve()
```