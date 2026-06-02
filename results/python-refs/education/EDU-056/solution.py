import json
import sys
from collections import defaultdict, deque

def topological_sort(topics):
    # Create adjacency list and in-degree count
    graph = defaultdict(list)
    in_degree = defaultdict(int)
    topic_map = {}
    
    # Build topic map and initialize in-degrees
    for topic in topics:
        topic_map[topic['id']] = topic
        in_degree[topic['id']] = 0
    
    # Build graph and calculate in-degrees
    for topic in topics:
        topic_id = topic['id']
        for dep in topic['depends_on']:
            graph[dep].append(topic_id)
            in_degree[topic_id] += 1
    
    # Find all nodes with no incoming edges
    queue = deque([tid for tid in topic_map.keys() if in_degree[tid] == 0])
    result = []
    
    while queue:
        current = queue.popleft()
        result.append(current)
        
        # Remove current node and update in-degrees
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result

def main():
    # Read input from stdin
    input_data = sys.stdin.read().strip()
    topics = json.loads(input_data)
    
    # Get topologically sorted order
    sorted_ids = topological_sort(topics)
    
    # Create topic lookup
    topic_map = {topic['id']: topic for topic in topics}
    
    # Generate output
    for topic_id in sorted_ids:
        topic = topic_map[topic_id]
        if topic['depends_on']:
            deps = ', '.join(topic['depends_on'])
            print(f"{topic_id}: {topic['title']} (requires: {deps})")
        else:
            print(f"{topic_id}: {topic['title']}")

if __name__ == "__main__":
    main()