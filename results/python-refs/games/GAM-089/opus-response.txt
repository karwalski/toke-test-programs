import sys
from collections import deque

def flood_fill(grid, start_row, start_col):
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    if start_row < 0 or start_row >= rows or start_col < 0 or start_col >= cols:
        return 0
    target_char = grid[start_row][start_col]
    visited = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    count = 0
    while queue:
        row, col = queue.popleft()
        count += 1
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < rows and 0 <= new_col < cols and 
                (new_row, new_col) not in visited and 
                new_col < len(grid[new_row]) and
                grid[new_row][new_col] == target_char):
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
    return count

data = sys.stdin.read().split('\n')
# Strip trailing empties
while data and data[-1] == '':
    data.pop()

# Last non-empty line is the coords
coord_line = data[-1]
parts = coord_line.split()
start_row, start_col = int(parts[0]), int(parts[1])

# Grid lines are everything before, excluding blank separator lines
grid_lines = data[:-1]
# Remove trailing blank lines from grid
while grid_lines and grid_lines[-1] == '':
    grid_lines.pop()

print(flood_fill(grid_lines, start_row, start_col))