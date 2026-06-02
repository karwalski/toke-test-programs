import json
import sys
from collections import defaultdict, deque

def solve_middleware_chain():
    input_data = sys.stdin.read().strip()
    middlewares = json.loads(input_data)
    
    # Build graph and in-degree count
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    all_names = set()
    
    # Collect all middleware names
    for middleware in middlewares:
        all_names.add(middleware["name"])
    
    # Initialize in-degree for all middlewares
    for name in all_names:
        in_degree[name] = 0
    
    # Build the dependency graph
    for middleware in middlewares:
        name = middleware["name"]
        
        # For each middleware that should come before this one
        for before_name in middleware["after"]:
            if before_name in all_names:
                graph[before_name].append(name)
                in_degree[name] += 1
        
        # For each middleware that should come after this one
        for after_name in middleware["before"]:
            if after_name in all_names:
                graph[name].append(after_name)
                in_degree[after_name] += 1
    
    # Topological sort using Kahn's algorithm
    queue = deque()
    result = []
    
    # Find all nodes with no incoming edges
    for name in all_names:
        if in_degree[name] == 0:
            queue.append(name)
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Remove this node from the graph
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check if we have a valid topological ordering
    if len(result) != len(all_names):
        print("CONFLICT: circular dependencies detected")
    else:
        print("VALID ORDER: " + ", ".join(result))

if __name__ == "__main__":
    solve_middleware_chain()