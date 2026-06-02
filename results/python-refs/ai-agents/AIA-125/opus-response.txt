import json
import sys

def solve_rollback(data):
    steps = data['steps']
    failed_step = data['failed_step']
    
    step_map = {step['id']: step for step in steps}
    
    # Find all steps that need rollback: failed step + all its (transitive) dependencies that are done
    to_rollback = set()
    
    def collect(step_id):
        if step_id in to_rollback:
            return
        if step_id not in step_map:
            return
        step = step_map[step_id]
        if step['status'] in ('done', 'failed'):
            to_rollback.add(step_id)
            for dep in step['depends_on']:
                collect(dep)
    
    collect(failed_step)
    
    # Order: reverse dependency order - things that depend on others come first
    # Topological sort where edge is dep -> dependent, output reversed
    # i.e., a step comes before its dependencies in the rollback order
    
    visited = set()
    order = []
    
    def dfs(step_id):
        if step_id in visited:
            return
        visited.add(step_id)
        # Visit dependents first... actually we want: step appears before its deps
        # So process step, then recurse into its deps
        # But need topological correctness
        pass
    
    # Better: build subgraph and do topo sort
    # Edge dep -> dependent means dependent must be rolled back before dep
    sub = list(to_rollback)
    in_deg = {s: 0 for s in sub}
    adj = {s: [] for s in sub}  # dependent -> deps (for rollback order edges)
    
    for s in sub:
        for dep in step_map[s]['depends_on']:
            if dep in to_rollback:
                # s depends on dep, so s must roll back before dep
                # edge s -> dep in rollback order
                adj[s].append(dep)
                in_deg[dep] += 1
    
    # Kahn's: nodes with in_deg 0 are those nothing depends on (top of chain)
    queue = [s for s in sub if in_deg[s] == 0]
    full_order = []
    while queue:
        # preserve some order
        current = queue.pop(0)
        full_order.append(current)
        for nxt in adj[current]:
            in_deg[nxt] -= 1
            if in_deg[nxt] == 0:
                queue.append(nxt)
    
    reversible_order = [s for s in full_order if step_map[s]['reversible']]
    non_reversible = [s for s in full_order if not step_map[s]['reversible']]
    
    return {
        "rollback_order": reversible_order,
        "non_reversible": non_reversible
    }

input_data = sys.stdin.read().strip()
data = json.loads(input_data)
result = solve_rollback(data)
print(json.dumps(result, separators=(',', ':')))