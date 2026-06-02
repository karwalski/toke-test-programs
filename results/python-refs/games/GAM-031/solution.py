import sys

def count_neighbors(grid, row, col, rows, cols):
    count = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr][nc] == '*':
                    count += 1
    return count

def next_generation(grid):
    rows = len(grid)
    cols = len(grid[0])
    new_grid = []
    
    for row in range(rows):
        new_row = []
        for col in range(cols):
            neighbors = count_neighbors(grid, row, col, rows, cols)
            current = grid[row][col]
            
            if current == '*':  # alive
                if neighbors == 2 or neighbors == 3:
                    new_row.append('*')
                else:
                    new_row.append('.')
            else:  # dead
                if neighbors == 3:
                    new_row.append('*')
                else:
                    new_row.append('.')
        new_grid.append(new_row)
    
    return new_grid

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Convert to grid
grid = []
for line in lines:
    grid.append(list(line))

# Compute next generation
next_grid = next_generation(grid)

# Output result
for row in next_grid:
    print(''.join(row))