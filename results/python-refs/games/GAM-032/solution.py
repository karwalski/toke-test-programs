import sys

def parse_grid(lines):
    grid = []
    for line in lines:
        line = line.strip()
        if line:
            grid.append(list(line))
    return grid

def get_neighbors(grid, row, col):
    rows, cols = len(grid), len(grid[0])
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
    rows, cols = len(grid), len(grid[0])
    new_grid = [['.' for _ in range(cols)] for _ in range(rows)]
    
    for r in range(rows):
        for c in range(cols):
            neighbors = get_neighbors(grid, r, c)
            if grid[r][c] == '*':
                if neighbors == 2 or neighbors == 3:
                    new_grid[r][c] = '*'
            else:
                if neighbors == 3:
                    new_grid[r][c] = '*'
    
    return new_grid

def grid_to_string(grid):
    return '\n'.join(''.join(row) for row in grid)

def solve():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    grid = parse_grid(lines)
    
    history = []
    current_grid = grid
    
    for generation in range(101):  # 0 to 100
        grid_str = grid_to_string(current_grid)
        
        # Check if we've seen this pattern before
        for i, past_grid in enumerate(history):
            if past_grid == grid_str:
                if i == len(history) - 1:
                    return "Stable"
                else:
                    period = len(history) - i
                    return f"Oscillator period {period}"
        
        history.append(grid_str)
        
        if generation < 100:
            current_grid = next_generation(current_grid)
    
    return "Chaotic"

print(solve())