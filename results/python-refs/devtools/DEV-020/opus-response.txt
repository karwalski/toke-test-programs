import sys
from collections import defaultdict

def find_cycles():
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
    
    cycles = []
    
    def dfs(start, node, path, visited_in_path):
        for neighbor in graph[node]:
            if neighbor == start:
                cycles.append(path + [neighbor])
            elif neighbor not in visited_in_path:
                visited_in_path.add(neighbor)
                dfs(start, neighbor, path + [neighbor], visited_in_path)
                visited_in_path.remove(neighbor)
    
    found = {}
    for node in sorted(nodes):
        dfs(node, node, [node], {node})
    
    # Deduplicate by canonical form
    unique = {}
    for cycle in cycles:
        nodes_in_cycle = cycle[:-1]
        # Find rotation starting with min
        min_idx = nodes_in_cycle.index(min(nodes_in_cycle))
        rotated = nodes_in_cycle[min_idx:] + nodes_in_cycle[:min_idx]
        key = tuple(rotated)
        if key not in unique or len(cycle) < len(unique[key]):
            unique[key] = rotated + [rotated[0]]
    
    if not unique:
        print("No circular dependencies found")
        return
    
    # Sort by first node, then length
    result = sorted(unique.values(), key=lambda c: (c[0], len(c)))
    for cycle in result:
        print(f"Cycle: {' -> '.join(cycle)}")

find_cycles()