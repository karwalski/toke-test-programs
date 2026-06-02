import sys

def read_sudoku():
    grid = []
    for _ in range(9):
        line = input().strip()
        row = []
        for char in line:
            if char == '.':
                row.append(0)
            else:
                row.append(int(char))
        grid.append(row)
    return grid

def get_candidates(grid, row, col):
    if grid[row][col] != 0:
        return set()
    
    used = set()
    
    # Check row
    for c in range(9):
        if grid[row][c] != 0:
            used.add(grid[row][c])
    
    # Check column
    for r in range(9):
        if grid[r][col] != 0:
            used.add(grid[r][col])
    
    # Check 3x3 box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for r in range(box_row, box_row + 3):
        for c in range(box_col, box_col + 3):
            if grid[r][c] != 0:
                used.add(grid[r][c])
    
    return set(range(1, 10)) - used

def find_naked_singles(grid):
    found = False
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) == 1:
                    grid[row][col] = candidates.pop()
                    found = True
    return found

def find_hidden_singles(grid):
    found = False
    
    # Check rows
    for row in range(9):
        for num in range(1, 10):
            if num not in grid[row]:
                possible_cols = []
                for col in range(9):
                    if grid[row][col] == 0 and num in get_candidates(grid, row, col):
                        possible_cols.append(col)
                if len(possible_cols) == 1:
                    grid[row][possible_cols[0]] = num
                    found = True
    
    # Check columns
    for col in range(9):
        for num in range(1, 10):
            column_values = [grid[r][col] for r in range(9)]
            if num not in column_values:
                possible_rows = []
                for row in range(9):
                    if grid[row][col] == 0 and num in get_candidates(grid, row, col):
                        possible_rows.append(row)
                if len(possible_rows) == 1:
                    grid[possible_rows[0]][col] = num
                    found = True
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            for num in range(1, 10):
                box_values = []
                for r in range(box_row, box_row + 3):
                    for c in range(box_col, box_col + 3):
                        box_values.append(grid[r][c])
                
                if num not in box_values:
                    possible_positions = []
                    for r in range(box_row, box_row + 3):
                        for c in range(box_col, box_col + 3):
                            if grid[r][c] == 0 and num in get_candidates(grid, r, c):
                                possible_positions.append((r, c))
                    if len(possible_positions) == 1:
                        r, c = possible_positions[0]
                        grid[r][c] = num
                        found = True
    
    return found

def is_solved(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return False
    return True

def has_naked_pairs(grid):
    # Check rows
    for row in range(9):
        candidates_by_col = {}
        for col in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) == 2:
                    candidates_tuple = tuple(sorted(candidates))
                    if candidates_tuple in candidates_by_col:
                        return True
                    candidates_by_col[candidates_tuple] = col
    
    # Check columns
    for col in range(9):
        candidates_by_row = {}
        for row in range(9):
            if grid[row][col] == 0:
                candidates = get_candidates(grid, row, col)
                if len(candidates) == 2:
                    candidates_tuple = tuple(sorted(candidates))
                    if candidates_tuple in candidates_by_row:
                        return True
                    candidates_by_row[candidates_tuple] = row
    
    return False

def rate_difficulty(grid):
    original_grid = [row[:] for row in grid]
    
    basic_techniques = 0
    advanced_techniques = 0
    
    while not is_solved(grid):
        progress = False
        
        # Try naked singles
        if find_naked_singles(grid):
            basic_techniques += 1
            progress = True
            continue
        
        # Try hidden singles
        if find_hidden_singles(grid):
            basic_techniques += 1
            progress = True
            continue
        
        # Check for advanced techniques needed
        if has_naked_pairs(grid):
            advanced_techniques += 1
        
        # If no progress with basic techniques, we need advanced ones
        if not progress:
            break
    
    # Rate based on techniques used
    if is_solved(grid) and basic_techniques > 0 and advanced_techniques == 0:
        return "Easy"
    elif basic_techniques > 0 and advanced_techniques <= 2:
        return "Medium"
    elif advanced_techniques <= 5:
        return "Hard"
    else:
        return "Expert"

def main():
    grid = read_sudoku()
    difficulty = rate_difficulty(grid)
    print(difficulty)

if __name__ == "__main__":
    main()