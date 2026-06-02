import sys
from collections import defaultdict

def find_eulerian_path(graph, edges):
    # Count degrees
    degrees = defaultdict(int)
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    
    # Check if Eulerian path exists
    odd_degree_nodes = [node for node, degree in degrees.items() if degree % 2 == 1]
    
    if len(odd_degree_nodes) not in [0, 2]:
        return None
    
    # Find starting node
    if len(odd_degree_nodes) == 2:
        start = odd_degree_nodes[0]
    else:
        start = next(iter(degrees.keys()))
    
    # Create adjacency list with edge tracking
    adj = defaultdict(list)
    edge_used = {}
    
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, i))
        adj[b].append((a, i))
        edge_used[i] = False
    
    # DFS to find Eulerian path
    path = []
    stack = [start]
    circuit = []
    
    while stack:
        curr = stack[-1]
        found_edge = False
        
        for neighbor, edge_idx in adj[curr]:
            if not edge_used[edge_idx]:
                edge_used[edge_idx] = True
                stack.append(neighbor)
                path.append((curr, neighbor, edge_idx))
                found_edge = True
                break
        
        if not found_edge:
            if stack:
                circuit.append(stack.pop())
    
    # Check if all edges were used
    if len(path) != len(edges):
        return None
    
    # Build result string
    result_parts = []
    for curr, next_node, edge_idx in path:
        result_parts.append(f"{curr}-{next_node}")
    
    return " ".join(result_parts)

def main():
    edges = []
    
    for line in sys.stdin:
        line = line.strip()
        if line:
            a, b = map(int, line.split())
            edges.append((a, b))
    
    if not edges:
        print("No valid chain")
        return
    
    # Create graph
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    
    result = find_eulerian_path(graph, edges)
    
    if result:
        print(f"Valid chain: {result}")
    else:
        print("No valid chain")

if __name__ == "__main__":
    main()