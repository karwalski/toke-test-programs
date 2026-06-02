import sys
from collections import defaultdict, deque

def find_cycles():
    # Read input and build graph
    graph = defaultdict(list)
    nodes = set()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(' -> ')
        if len(parts) != 2:
            continue
            
        source, target = parts[0].strip(), parts[1].strip()
        graph[source].append(target)
        nodes.add(source)
        nodes.add(target)
    
    # DFS to find cycles
    def dfs(node, path, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        
        for neighbor in graph[node]:
            if neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                return cycle
            
            if neighbor not in visited:
                result = dfs(neighbor, path, visited, rec_stack)
                if result:
                    return result
        
        path.pop()
        rec_stack.remove(node)
        return None
    
    # Check each node for cycles
    visited = set()
    for node in nodes:
        if node not in visited:
            cycle = dfs(node, [], visited, set())
            if cycle:
                cycle_str = ' -> '.join(cycle)
                print(f"Cycle: {cycle_str}")
                return
    
    print("No circular dependencies found")

find_cycles()