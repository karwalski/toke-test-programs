from collections import defaultdict, deque

def hopcroft_karp(graph, u_count, v_count):
    # Initialize matching
    pair_u = [-1] * u_count  # pair_u[u] = v if u is matched to v, else -1
    pair_v = [-1] * v_count  # pair_v[v] = u if v is matched to u, else -1
    dist = [0] * u_count
    
    def bfs():
        queue = deque()
        for u in range(u_count):
            if pair_u[u] == -1:
                dist[u] = 0
                queue.append(u)
            else:
                dist[u] = float('inf')
        
        dist_nil = float('inf')
        
        while queue:
            u = queue.popleft()
            if dist[u] < dist_nil:
                for v in graph[u]:
                    if pair_v[v] == -1:
                        if dist_nil == float('inf'):
                            dist_nil = dist[u] + 1
                    else:
                        if dist[pair_v[v]] == float('inf'):
                            dist[pair_v[v]] = dist[u] + 1
                            queue.append(pair_v[v])
        
        return dist_nil != float('inf')
    
    def dfs(u):
        if u != -1:
            for v in graph[u]:
                if pair_v[v] == -1 or (dist[pair_v[v]] == dist[u] + 1 and dfs(pair_v[v])):
                    pair_v[v] = u
                    pair_u[u] = v
                    return True
            dist[u] = float('inf')
            return False
        return True
    
    matching = 0
    while bfs():
        for u in range(u_count):
            if pair_u[u] == -1 and dfs(u):
                matching += 1
    
    return matching, pair_u

# Read input
line = input().split()
u_count, v_count, e_count = int(line[0]), int(line[1]), int(line[2])

graph = defaultdict(list)
for _ in range(e_count):
    u, v = map(int, input().split())
    graph[u].append(v)

# Find maximum matching
max_matching, pair_u = hopcroft_karp(graph, u_count, v_count)

# Output the result
matching_pairs = []
for u in range(u_count):
    if pair_u[u] != -1:
        matching_pairs.append(f"{u}-{pair_u[u]}")

print("Matching:", " ".join(matching_pairs))
print(f"Size: {max_matching}")