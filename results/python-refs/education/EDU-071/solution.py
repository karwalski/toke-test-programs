import json
import sys
from collections import defaultdict, deque

def topological_sort(dependencies):
    # Build graph and in-degree count
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    all_concepts = set()
    
    for item in dependencies:
        concept = item["concept"]
        prerequisite = item["must_know_first"]
        
        all_concepts.add(concept)
        if prerequisite:
            all_concepts.add(prerequisite)
            graph[prerequisite].append(concept)
            in_degree[concept] += 1
        else:
            in_degree[concept] = in_degree.get(concept, 0)
    
    # Initialize in-degree for all concepts
    for concept in all_concepts:
        if concept not in in_degree:
            in_degree[concept] = 0
    
    # Find all nodes with no incoming edges
    queue = deque([concept for concept in all_concepts if in_degree[concept] == 0])
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Remove edges from current node
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result

# Read input from stdin
input_data = sys.stdin.read().strip()
dependencies = json.loads(input_data)

# Get topologically sorted order
sorted_concepts = topological_sort(dependencies)

# Output in required format
for i, concept in enumerate(sorted_concepts, 1):
    print(f"{i}. {concept}")