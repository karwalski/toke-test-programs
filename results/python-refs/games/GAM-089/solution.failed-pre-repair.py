import sys
from collections import deque

def flood_fill(grid, start_row, start_col):
    if not grid or not grid[0]:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    
    # Check if starting position is valid
    if start_row < 0 or start_row >= rows or start_col < 0 or start_col >= cols:
        return 0
    
    # Get the character we're looking for
    target_char = grid[start_row][start_col]
    visited = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))
    
    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    count = 0
    
    while queue:
        row, col = queue.popleft()
        count += 1
        
        # Check all 4 directions
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check bounds and if already visited
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                (new_row, new_col) not in visited and 
                grid[new_row][new_col] == target_char):
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
    
    return count

# Read input
lines = []
start_row = start_col = None

for line in sys.stdin:
    line = line.rstrip('\n')
    
    # Skip empty lines
    if not line:
        continue
    
    # Try to parse as coordinates
    try:
        parts = line.split()
        if len(parts) == 2 and all(part.lstrip('-').isdigit() for part in parts):
            start_row, start_col = int(parts[0]), int(parts[1])
            break
    except (ValueError, IndexError):
        pass
    
    # If we get here, it's a grid line
    lines.append(line)

grid = lines

# Validate that we got the starting position
if start_row is None or start_col is None:
    print(0)
else:
    # Calculate and output the result
    result = flood_fill(grid, start_row, start_col)
    print(result)