import sys
from collections import defaultdict

def read_grid():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            lines.append(list(map(int, line.split())))
    return lines

def is_power_of_2(n):
    return n > 0 and (n & (n - 1)) == 0

def validate_tromino_tiling(grid):
    n = len(grid)
    
    # Check if grid is square
    if not all(len(row) == n for row in grid):
        return "Invalid: grid is not square"
    
    # Check if n is a power of 2
    if not is_power_of_2(n):
        return "Invalid: grid size is not a power of 2"
    
    # Count missing squares (0s)
    missing_count = sum(row.count(0) for row in grid)
    if missing_count != 1:
        return "Invalid: must have exactly one missing square"
    
    # Group cells by tromino ID
    trominos = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if grid[i][j] != 0:
                trominos[grid[i][j]].append((i, j))
    
    # Check each tromino
    for tromino_id, cells in trominos.items():
        # Each tromino must have exactly 3 cells
        if len(cells) != 3:
            return f"Invalid: tromino {tromino_id} does not have exactly 3 cells"
        
        # Check if the 3 cells form a valid L-tromino shape
        if not is_valid_l_tromino(cells):
            return f"Invalid: tromino {tromino_id} is not a valid L-shape"
    
    # Check if all cells are covered (except the missing one)
    total_cells = n * n
    expected_trominos = (total_cells - 1) // 3
    if len(trominos) != expected_trominos:
        return "Invalid: incorrect number of trominos"
    
    return "Valid"

def is_valid_l_tromino(cells):
    """Check if 3 cells form a valid L-tromino"""
    if len(cells) != 3:
        return False
    
    # Sort cells by coordinates
    cells = sorted(cells)
    
    # Extract coordinates
    rows = [cell[0] for cell in cells]
    cols = [cell[1] for cell in cells]
    
    # Check if all cells are adjacent and form L-shape
    # Valid L-tromino patterns (relative positions):
    # Pattern 1: (0,0), (0,1), (1,0)
    # Pattern 2: (0,0), (0,1), (1,1)  
    # Pattern 3: (0,0), (1,0), (1,1)
    # Pattern 4: (0,1), (1,0), (1,1)
    
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Must fit in 2x2 square
    if max_row - min_row > 1 or max_col - min_col > 1:
        return False
    
    # Convert to relative coordinates
    relative = [(r - min_row, c - min_col) for r, c in cells]
    relative = sorted(relative)
    
    # Check against valid L-tromino patterns
    valid_patterns = [
        [(0,0), (0,1), (1,0)],  # L shape
        [(0,0), (0,1), (1,1)],  # L shape rotated
        [(0,0), (1,0), (1,1)],  # L shape rotated
        [(0,1), (1,0), (1,1)]   # L shape rotated
    ]
    
    return relative in valid_patterns

def main():
    grid = read_grid()
    result = validate_tromino_tiling(grid)
    print(result)

if __name__ == "__main__":
    main()