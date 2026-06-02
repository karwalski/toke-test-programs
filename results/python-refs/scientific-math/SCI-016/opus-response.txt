import heapq

def dijkstra(graph, source, V):
    dist = [float('inf')] * V
    prev = [None] * V
    dist[source] = 0
    pq = [(0, source)]
    visited = set()
    while pq:
        current_dist, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, weight in graph.get(u, []):
            if v not in visited:
                new_dist = current_dist + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(pq, (new_dist, v))
    return dist, prev

def reconstruct_path(prev, source, target):
    if prev[target] is None and target != source:
        return None
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return path

line = input().split()
V, E = int(line[0]), int(line[1])
graph = {}
for _ in range(E):
    u, v, w = map(int, input().split())
    if u not in graph:
        graph[u] = []
    graph[u].append((v, w))

source = int(input())
distances, previous = dijkstra(graph, source, V)

for node in range(V):
    if distances[node] == float('inf'):
        print(f"{node}: INF")
    else:
        path = reconstruct_path(previous, source, node)
        path_str = "[" + ",".join(str(x) for x in path) + "]"
        print(f"{node}: {distances[node]} {path_str}")