def solve():
    # Read input
    v, e = map(int, input().split())
    
    # Build adjacency list
    adj = [[] for _ in range(v)]
    for _ in range(e):
        u, v_node = map(int, input().split())
        adj[u].append(v_node)
        adj[v_node].append(u)
    
    # Initialize colors array
    colors = [-1] * v
    
    # Color each vertex using greedy algorithm
    for node in range(v):
        # Find colors used by adjacent vertices
        used_colors = set()
        for neighbor in adj[node]:
            if colors[neighbor] != -1:
                used_colors.add(colors[neighbor])
        
        # Find minimum available color
        color = 0
        while color in used_colors:
            color += 1
        
        colors[node] = color
    
    # Output the coloring
    coloring_parts = []
    for i in range(v):
        coloring_parts.append(f"{i}={colors[i]}")
    
    print("Colouring: " + " ".join(coloring_parts))
    
    # Output number of colors used
    max_color = max(colors)
    print(f"Colours used: {max_color + 1}")

solve()