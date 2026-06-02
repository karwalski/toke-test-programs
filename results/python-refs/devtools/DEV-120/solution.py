import json
import sys
from collections import defaultdict, deque

def main():
    # Read input from stdin
    input_data = json.load(sys.stdin)
    targets = input_data["targets"]
    changed_files = set(input_data["changed_files"])
    
    # Build target lookup
    target_map = {target["name"]: target for target in targets}
    
    # Build reverse dependency graph (who depends on each target)
    reverse_deps = defaultdict(list)
    for target in targets:
        for dep in target["depends_on"]:
            reverse_deps[dep].append(target["name"])
    
    # Find targets that need rebuilding
    needs_rebuild = {}  # target_name -> reason
    
    # Check for direct input changes
    for target in targets:
        target_name = target["name"]
        target_inputs = set(target["inputs"])
        if target_inputs & changed_files:  # intersection
            needs_rebuild[target_name] = "input changed"
    
    # Propagate changes through dependencies using BFS
    queue = deque(needs_rebuild.keys())
    while queue:
        current = queue.popleft()
        for dependent in reverse_deps[current]:
            if dependent not in needs_rebuild:
                needs_rebuild[dependent] = f"dependency {current} changed"
                queue.append(dependent)
    
    # If no targets need rebuilding, output nothing
    if not needs_rebuild:
        return
    
    # Topological sort to get dependency order
    def topological_sort():
        # Build dependency graph for targets that need rebuilding
        in_degree = defaultdict(int)
        graph = defaultdict(list)
        
        rebuild_targets = set(needs_rebuild.keys())
        
        for target_name in rebuild_targets:
            target = target_map[target_name]
            for dep in target["depends_on"]:
                if dep in rebuild_targets:
                    graph[dep].append(target_name)
                    in_degree[target_name] += 1
            # Ensure all targets are in in_degree
            if target_name not in in_degree:
                in_degree[target_name] = 0
        
        # Kahn's algorithm
        queue = deque([target for target in rebuild_targets if in_degree[target] == 0])
        result = []
        
        while queue:
            current = queue.popleft()
            result.append(current)
            
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        return result
    
    # Get sorted targets
    sorted_targets = topological_sort()
    
    # Output results
    print("Needs rebuild:")
    for i, target_name in enumerate(sorted_targets, 1):
        reason = needs_rebuild[target_name]
        print(f"{i}. {target_name} ({reason})")

if __name__ == "__main__":
    main()