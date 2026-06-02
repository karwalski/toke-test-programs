def is_valid_sudoku(grid):
    # Check rows
    for row in grid:
        if sorted(row) != list(range(1, 10)):
            return False
    
    # Check columns
    for col in range(9):
        column = [grid[row][col] for row in range(9)]
        if sorted(column) != list(range(1, 10)):
            return False
    
    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
        for box_col in range(0, 9, 3):
            box = []
            for r in range(box_row, box_row + 3):
                for c in range(box_col, box_col + 3):
                    box.append(grid[r][c])
            if sorted(box) != list(range(1, 10)):
                return False
    
    return True

# Read input
grid = []
for _ in range(9):
    line = input().strip()
    row = [int(digit) for digit in line]
    grid.append(row)

# Validate and output result
if is_valid_sudoku(grid):
    print("Valid")
else:
    print("Invalid")