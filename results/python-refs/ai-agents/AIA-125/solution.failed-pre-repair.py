import json
import sys

def solve_rollback(data):
    steps = data['steps']
    failed_step = data['failed_step']
    
    # Create a mapping of step_id to step info
    step_map = {step['id']: step for step in steps}
    
    # Build dependency graph (what depends on what)
    dependents = {}  # step_id -> list of steps that depend on it
    for step in steps:
        for dep in step['depends_on']:
            if dep not in dependents:
                dependents[dep] = []
            dependents[dep].append(step['id'])
    
    # Find all steps that need rollback
    # Start with failed step and traverse up the dependency chain
    def find_steps_to_rollback(step_id, visited):
        if step_id in visited:
            return set()
        
        visited.add(step_id)
        steps_to_rollback = set()
        
        step = step_map[step_id]
        # Add current step if it's done or failed
        if step['status'] in ['done', 'failed']:
            steps_to_rollback.add(step_id)
            
            # Add all dependencies that are done
            for dep in step['depends_on']:
                if dep in step_map and step_map[dep]['status'] == 'done':
                    steps_to_rollback.update(find_steps_to_rollback(dep, visited.copy()))
        
        return steps_to_rollback
    
    steps_to_rollback = find_steps_to_rollback(failed_step, set())
    
    # Separate reversible and non-reversible steps
    reversible_steps = []
    non_reversible_steps = []
    
    for step_id in steps_to_rollback:
        step = step_map[step_id]
        if step['reversible']:
            reversible_steps.append(step_id)
        else:
            non_reversible_steps.append(step_id)
    
    # Order reversible steps for rollback (reverse topological order)
    def topological_sort_reverse(steps_list):
        # Build subgraph of steps to rollback
        sub_dependents = {}
        for step_id in steps_list:
            sub_dependents[step_id] = []
            if step_id in dependents:
                for dependent in dependents[step_id]:
                    if dependent in steps_list:
                        sub_dependents[step_id].append(dependent)
        
        # Calculate in-degrees in the subgraph
        in_degree = {step_id: 0 for step_id in steps_list}
        for step_id in steps_list:
            for dependent in sub_dependents[step_id]:
                in_degree[dependent] += 1
        
        # Reverse topological sort (start with nodes that have no dependents)
        result = []
        queue = [step_id for step_id in steps_list if len(sub_dependents[step_id]) == 0]
        
        while queue:
            current = queue.pop(0)
            result.append(current)
            
            # Find what current depends on
            current_step = step_map[current]
            for dep in current_step['depends_on']:
                if dep in steps_list:
                    in_degree[dep] -= 1
                    if in_degree[dep] == 0:
                        queue.append(dep)
        
        return result
    
    rollback_order = topological_sort_reverse(reversible_steps)
    
    return {
        "rollback_order": rollback_order,
        "non_reversible": sorted(non_reversible_steps)
    }

# Read input from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

# Solve and output
result = solve_rollback(data)
print(json.dumps(result, separators=(',', ':')))