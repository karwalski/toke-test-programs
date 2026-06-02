def is_valid(grid, row, col, num):
    # Check row
    for j in range(9):
        if grid[row][j] == num:
            return False
    
    # Check column
    for i in range(9):
        if grid[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    
    return True

def get_candidates(grid, row, col):
    candidates = []
    for num in range(1, 10):
        if is_valid(grid, row, col, num):
            candidates.append(num)
    return candidates

def propagate_constraints(grid):
    changed = True
    while changed:
        changed = False
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    candidates = get_candidates(grid, i, j)
                    if len(candidates) == 1:
                        grid[i][j] = candidates[0]
                        changed = True
                    elif len(candidates) == 0:
                        return False
    return True

def find_best_cell(grid):
    min_candidates = 10
    best_cell = None
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (i, j)
                    if min_candidates == 0:
                        return best_cell
    
    return best_cell

def solve_sudoku(grid):
    if not propagate_constraints(grid):
        return False
    
    cell = find_best_cell(grid)
    if cell is None:
        return True
    
    row, col = cell
    candidates = get_candidates(grid, row, col)
    
    for num in candidates:
        # Make a copy of the grid
        grid_copy = [row[:] for row in grid]
        grid_copy[row][col] = num
        
        if solve_sudoku(grid_copy):
            # Copy solution back to original grid
            for i in range(9):
                for j in range(9):
                    grid[i][j] = grid_copy[i][j]
            return True
    
    return False

def print_grid(grid):
    for row in grid:
        print(' '.join(map(str, row)))

# Read input
grid = []
for _ in range(9):
    line = input().strip()
    row = [int(c) for c in line]
    grid.append(row)

# Solve the puzzle
if solve_sudoku(grid):
    print_grid(grid)
else:
    print("NO SOLUTION")