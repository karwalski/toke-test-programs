import sys
from collections import defaultdict, deque

def parse_dependencies():
    dependencies = {}
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        parts = line.split(':')
        package = parts[0].strip()
        deps = []
        if len(parts) > 1 and parts[1].strip():
            deps = parts[1].strip().split()
        dependencies[package] = deps
    
    return dependencies

def find_circular_dependency(graph, package, visited, rec_stack, path):
    visited.add(package)
    rec_stack.add(package)
    path.append(package)
    
    for dep in graph.get(package, []):
        if dep not in visited:
            cycle = find_circular_dependency(graph, dep, visited, rec_stack, path)
            if cycle:
                return cycle
        elif dep in rec_stack:
            # Found cycle - build the cycle path
            cycle_start = path.index(dep)
            cycle_path = path[cycle_start:] + [dep]
            return cycle_path
    
    rec_stack.remove(package)
    path.pop()
    return None

def topological_sort(dependencies):
    # Build graph and find all packages
    graph = defaultdict(list)
    all_packages = set()
    
    for package, deps in dependencies.items():
        all_packages.add(package)
        for dep in deps:
            graph[package].append(dep)
            all_packages.add(dep)
    
    # Check for circular dependencies
    visited = set()
    for package in all_packages:
        if package not in visited:
            cycle = find_circular_dependency(graph, package, visited, set(), [])
            if cycle:
                cycle_str = " -> ".join(cycle)
                return f"Circular dependency detected: {cycle_str}"
    
    # Perform topological sort using DFS
    visited = set()
    result = []
    
    def dfs(package):
        if package in visited:
            return
        visited.add(package)
        
        for dep in graph.get(package, []):
            dfs(dep)
        
        result.append(package)
    
    for package in all_packages:
        dfs(package)
    
    return result

def main():
    dependencies = parse_dependencies()
    result = topological_sort(dependencies)
    
    if isinstance(result, str):
        print(result)
    else:
        print("Install order:")
        for i, package in enumerate(result, 1):
            print(f"{i}. {package}")

if __name__ == "__main__":
    main()