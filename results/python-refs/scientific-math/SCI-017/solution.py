import heapq
from collections import defaultdict

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_neighbors(pos, rows, cols):
    r, c = pos
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def a_star(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    
    # Priority queue: (f_score, position)
    open_set = [(0, start)]
    
    # Dictionaries to track costs and paths
    g_score = defaultdict(lambda: float('inf'))
    g_score[start] = 0
    
    f_score = defaultdict(lambda: float('inf'))
    f_score[start] = manhattan_distance(start, end)
    
    came_from = {}
    
    while open_set:
        current_f, current = heapq.heappop(open_set)
        
        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[end]
        
        for neighbor in get_neighbors(current, rows, cols):
            nr, nc = neighbor
            
            # Skip walls
            if grid[nr][nc] == '#':
                continue
            
            tentative_g = g_score[current] + 1
            
            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + manhattan_distance(neighbor, end)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None, 0

# Read input
rows, cols = map(int, input().split())
grid = []
for _ in range(rows):
    grid.append(input().strip())

start_row, start_col = map(int, input().split())
end_row, end_col = map(int, input().split())

start = (start_row, start_col)
end = (end_row, end_col)

# Find path
path, cost = a_star(grid, start, end)

if path is None:
    print("NO PATH")
else:
    path_str = " ".join(f"({r},{c})" for r, c in path)
    print(f"Path: {path_str} Cost: {cost}")