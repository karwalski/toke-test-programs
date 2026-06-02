def find_hamiltonian_path(graph, start, V):
    def backtrack(path, visited):
        if len(path) == V:
            return path
        
        current = path[-1]
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                
                result = backtrack(path, visited)
                if result:
                    return result
                
                path.pop()
                visited.remove(neighbor)
        
        return None
    
    visited = {start}
    path = [start]
    return backtrack(path, visited)

# Read input
V, E = map(int, input().split())

# Initialize adjacency list
graph = {i: [] for i in range(V)}

# Read edges
for _ in range(E):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(u)

# Read start vertex
start = int(input())

# Find Hamiltonian path
result = find_hamiltonian_path(graph, start, V)

if result:
    print("Path:", " ".join(map(str, result)))
else:
    print("NO HAMILTONIAN PATH")