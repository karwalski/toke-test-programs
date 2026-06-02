import sys

def is_valid(grid, row, col, num):
    for j in range(9):
        if grid[row][j] == num:
            return False
    for i in range(9):
        if grid[i][col] == num:
            return False
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if grid[i][j] == num:
                return False
    return True

def get_candidates(grid, row, col):
    return [num for num in range(1, 10) if is_valid(grid, row, col, num)]

def find_best_cell(grid):
    min_candidates = 10
    best_cell = None
    best_cands = None
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                candidates = get_candidates(grid, i, j)
                if len(candidates) < min_candidates:
                    min_candidates = len(candidates)
                    best_cell = (i, j)
                    best_cands = candidates
                    if min_candidates <= 1:
                        return best_cell, best_cands
    return best_cell, best_cands

backtracks = 0

def solve_sudoku(grid):
    global backtracks
    cell, candidates = find_best_cell(grid)
    if cell is None:
        return True
    row, col = cell
    if not candidates:
        return False
    for num in candidates:
        grid[row][col] = num
        if solve_sudoku(grid):
            return True
        grid[row][col] = 0
        backtracks += 1
    return False

def main():
    data = sys.stdin.read().split()
    grid = []
    for line in data[:9]:
        grid.append([int(c) for c in line])
    if solve_sudoku(grid):
        for row in grid:
            print(' '.join(map(str, row)))
    else:
        print("NO SOLUTION")
    sys.stderr.write(f"Backtracks: {backtracks}\n")

main()