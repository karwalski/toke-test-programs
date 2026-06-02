import json
import sys
from collections import defaultdict, deque

def validate_workflow(data):
    nodes = data.get('nodes', [])
    
    # Extract node IDs and dependencies
    node_ids = set()
    dependencies = {}
    
    for node in nodes:
        node_id = node.get('id')
        depends_on = node.get('depends_on', [])
        
        if node_id is None:
            return {"valid": False, "errors": ["Node missing 'id' field"], "execution_order": []}
        
        node_ids.add(node_id)
        dependencies[node_id] = depends_on
    
    errors = []
    
    # Check for missing dependencies
    for node_id, deps in dependencies.items():
        for dep in deps:
            if dep not in node_ids:
                errors.append(f"Node '{node_id}' depends on missing node '{dep}'")
    
    if errors:
        return {"valid": False, "errors": errors, "execution_order": []}
    
    # Build adjacency list for graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    
    # Initialize in_degree for all nodes
    for node_id in node_ids:
        in_degree[node_id] = 0
    
    # Build graph and calculate in-degrees
    for node_id, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(node_id)
            in_degree[node_id] += 1
    
    # Topological sort using Kahn's algorithm
    queue = deque()
    execution_order = []
    
    # Find nodes with no incoming edges
    for node_id in node_ids:
        if in_degree[node_id] == 0:
            queue.append(node_id)
    
    while queue:
        current = queue.popleft()
        execution_order.append(current)
        
        # Remove edges from current node
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles
    if len(execution_order) != len(node_ids):
        cycle_nodes = [node for node in node_ids if node not in execution_order]
        errors.append(f"Cycle detected involving nodes: {sorted(cycle_nodes)}")
        return {"valid": False, "errors": errors, "execution_order": []}
    
    # Check for unreachable nodes (nodes that cannot be reached from root nodes)
    root_nodes = [node_id for node_id in node_ids if not dependencies[node_id]]
    
    if not root_nodes:
        errors.append("No root nodes found (all nodes have dependencies)")
        return {"valid": False, "errors": errors, "execution_order": []}
    
    # Find all reachable nodes from root nodes
    reachable = set()
    queue = deque(root_nodes)
    
    while queue:
        current = queue.popleft()
        if current not in reachable:
            reachable.add(current)
            for neighbor in graph[current]:
                if neighbor not in reachable:
                    queue.append(neighbor)
    
    unreachable_nodes = node_ids - reachable
    if unreachable_nodes:
        errors.append(f"Unreachable nodes: {sorted(unreachable_nodes)}")
        return {"valid": False, "errors": errors, "execution_order": []}
    
    return {"valid": True, "errors": [], "execution_order": execution_order}

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Validate workflow
result = validate_workflow(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))