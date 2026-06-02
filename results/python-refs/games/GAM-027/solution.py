import heapq
import sys

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    
    # Priority queue: (f_score, g_score, position)
    open_set = [(0, 0, start)]
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while open_set:
        current_f, current_g, current = heapq.heappop(open_set)
        
        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            
            # Check bounds
            if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and 
                grid[neighbor[0]][neighbor[1]] != '#'):
                
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g, neighbor))
    
    return None

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Parse grid
grid = []
i = 0
while i < len(lines) and lines[i] != '':
    grid.append(lines[i])
    i += 1

# Skip blank line
i += 1

# Parse start and end
start_parts = lines[i].split()
start = (int(start_parts[1]), int(start_parts[2]))

end_parts = lines[i+1].split()
end = (int(end_parts[1]), int(end_parts[2]))

# Find path
path = astar(grid, start, end)

if path is None:
    print("No path")
else:
    print(len(path))
    
    # Create result grid
    result_grid = [list(row) for row in grid]
    for pos in path:
        result_grid[pos[0]][pos[1]] = '*'
    
    # Print result grid
    for row in result_grid:
        print(''.join(row))