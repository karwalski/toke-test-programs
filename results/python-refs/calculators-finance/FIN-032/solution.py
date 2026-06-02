import sys
from collections import defaultdict, deque

def find_conversion_path(graph, start, end):
    if start == end:
        return [start], 1.0
    
    queue = deque([(start, [start], 1.0)])
    visited = set([start])
    
    while queue:
        current, path, rate = queue.popleft()
        
        for neighbor, exchange_rate in graph[current]:
            if neighbor not in visited:
                new_rate = rate * exchange_rate
                new_path = path + [neighbor]
                
                if neighbor == end:
                    return new_path, new_rate
                
                visited.add(neighbor)
                queue.append((neighbor, new_path, new_rate))
    
    return None, 0.0

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse first line
    first_line = lines[0].split()
    amount = float(first_line[0])
    source = first_line[1]
    target = first_line[2]
    
    # Build graph of currency exchanges
    graph = defaultdict(list)
    
    for i in range(1, len(lines)):
        if lines[i]:
            parts = lines[i].split()
            cur1 = parts[0]
            cur2 = parts[1]
            rate = float(parts[2])
            
            # Add bidirectional edges
            graph[cur1].append((cur2, rate))
            graph[cur2].append((cur1, 1.0 / rate))
    
    # Find conversion path
    path, conversion_rate = find_conversion_path(graph, source, target)
    
    if path:
        result = amount * conversion_rate
        print(f"{result:.2f}")
        print("->".join(path))

if __name__ == "__main__":
    main()