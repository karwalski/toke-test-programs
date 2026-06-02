import json
import sys
from collections import defaultdict, deque

def solve_dependencies(tool_calls):
    # Create a mapping from id to tool call
    tools = {tool['id']: tool for tool in tool_calls}
    
    # Create dependency graph
    dependencies = defaultdict(set)
    dependents = defaultdict(set)
    
    for tool in tool_calls:
        tool_id = tool['id']
        for dep in tool['depends_on']:
            dependencies[tool_id].add(dep)
            dependents[dep].add(tool_id)
    
    # Find tools with no dependencies to start
    ready = deque()
    for tool in tool_calls:
        if not tool['depends_on']:
            ready.append(tool['id'])
    
    batches = []
    remaining_deps = {tool['id']: set(tool['depends_on']) for tool in tool_calls}
    
    while ready or any(remaining_deps.values()):
        if not ready:
            break
            
        # Current batch contains all ready tools
        current_batch = list(ready)
        ready.clear()
        batches.append(current_batch)
        
        # After this batch completes, update dependencies
        for completed_tool in current_batch:
            # Remove this tool from remaining dependencies
            if completed_tool in remaining_deps:
                del remaining_deps[completed_tool]
            
            # Check which tools are now ready
            for dependent in dependents[completed_tool]:
                if dependent in remaining_deps:
                    remaining_deps[dependent].discard(completed_tool)
                    if not remaining_deps[dependent]:
                        ready.append(dependent)
    
    return batches

# Read input from stdin
input_data = json.loads(sys.stdin.read().strip())

# Solve dependencies
result = solve_dependencies(input_data)

# Output result as JSON
print(json.dumps(result, separators=(',', ':')))