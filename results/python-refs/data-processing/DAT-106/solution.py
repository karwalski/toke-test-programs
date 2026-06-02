import json
import sys
from collections import defaultdict, deque

def build_lineage_graph(transformations):
    # Build directed graph: table -> list of tables it directly affects
    graph = defaultdict(list)
    
    for step in transformations:
        if 'input' in step and 'output' in step:
            input_table = step['input']
            output_table = step['output']
            graph[input_table].append(output_table)
    
    return graph

def find_all_affected_tables(graph, start_table):
    # BFS to find all tables transitively affected by start_table
    visited = set()
    queue = deque([start_table])
    affected = []
    
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        
        # Add direct dependencies to queue and results
        for dependent in graph[current]:
            if dependent not in visited:
                queue.append(dependent)
                affected.append(dependent)
    
    return affected

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse input
    transformations = json.loads(lines[0])
    impact_command = lines[1].split()
    target_table = impact_command[1]
    
    # Build lineage graph
    graph = build_lineage_graph(transformations)
    
    # Find all affected tables
    affected_tables = find_all_affected_tables(graph, target_table)
    
    # Output lineage graph as JSON
    lineage_output = {target_table: affected_tables}
    print(json.dumps(lineage_output, separators=(',', ':')))
    
    # Output impact analysis
    if affected_tables:
        print(f"Tables affected by {target_table}: {', '.join(affected_tables)}")
    else:
        print(f"Tables affected by {target_table}: ")

if __name__ == "__main__":
    main()