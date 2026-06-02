import sys
from collections import defaultdict

def dfs(graph, node, visited, rec_stack, post_order):
    visited[node] = True
    rec_stack[node] = True
    
    for neighbor in graph[node]:
        if not visited[neighbor]:
            if dfs(graph, neighbor, visited, rec_stack, post_order):
                return True
        elif rec_stack[neighbor]:
            return True
    
    rec_stack[node] = False
    post_order.append(node)
    return False

def topological_sort(v, edges):
    graph = defaultdict(list)
    
    for u, v_node in edges:
        graph[u].append(v_node)
    
    visited = [False] * v
    rec_stack = [False] * v
    post_order = []
    
    for i in range(v):
        if not visited[i]:
            if dfs(graph, i, visited, rec_stack, post_order):
                return "CYCLE"
    
    post_order.reverse()
    return " ".join(map(str, post_order))

# Read input
line = input().strip().split()
v, e = int(line[0]), int(line[1])

edges = []
for _ in range(e):
    u, v_node = map(int, input().strip().split())
    edges.append((u, v_node))

# Solve and output
result = topological_sort(v, edges)
print(f"Topological order: {result}")