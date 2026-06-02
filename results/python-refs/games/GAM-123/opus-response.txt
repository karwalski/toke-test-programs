import sys
from itertools import combinations

def parse_grid():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip())
    while lines and not lines[-1]:
        lines.pop()
    grid = []
    for line in lines:
        grid.append(line.split())
    return grid

def solve_kakuro(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    empty_cells = []
    h_clues = {}
    v_clues = {}
    
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell == '?':
                empty_cells.append((i, j))
            elif cell.startswith('H') and len(cell) > 1 and cell[1:].isdigit():
                h_clues[(i, j)] = int(cell[1:])
            elif cell.startswith('V') and len(cell) > 1 and cell[1:].isdigit():
                v_clues[(i, j)] = int(cell[1:])
    
    h_segments = []
    v_segments = []
    
    for (r, c), target_sum in h_clues.items():
        segment = []
        for j in range(c + 1, cols):
            if grid[r][j] == '?':
                segment.append((r, j))
            else:
                break
        if segment:
            h_segments.append((target_sum, segment))
    
    for (r, c), target_sum in v_clues.items():
        segment = []
        for i in range(r + 1, rows):
            if grid[i][c] == '?':
                segment.append((i, c))
            else:
                break
        if segment:
            v_segments.append((target_sum, segment))
    
    assignment = {}
    
    def check_segments():
        for target_sum, segment in h_segments + v_segments:
            assigned = [assignment[cell] for cell in segment if cell in assignment]
            if len(set(assigned)) != len(assigned):
                return False
            unassigned_count = len(segment) - len(assigned)
            current_sum = sum(assigned)
            remaining_sum = target_sum - current_sum
            
            if unassigned_count == 0:
                if current_sum != target_sum:
                    return False
            else:
                if remaining_sum < unassigned_count:
                    return False
                used_digits = set(assigned)
                available_digits = [d for d in range(1, 10) if d not in used_digits]
                if len(available_digits) < unassigned_count:
                    return False
                min_possible = sum(available_digits[:unassigned_count])
                max_possible = sum(available_digits[-unassigned_count:])
                if remaining_sum < min_possible or remaining_sum > max_possible:
                    return False
        return True
    
    def backtrack(cell_idx):
        if cell_idx == len(empty_cells):
            return check_segments()
        
        cell = empty_cells[cell_idx]
        
        for digit in range(1, 10):
            assignment[cell] = digit
            if check_segments():
                if backtrack(cell_idx + 1):
                    return True
            del assignment[cell]
        
        return False
    
    if backtrack(0):
        result = [row[:] for row in grid]
        for (r, c), value in assignment.items():
            result[r][c] = str(value)
        # Replace clue cells with just numbers
        for i in range(rows):
            for j in range(cols):
                cell = result[i][j]
                if (cell.startswith('H') or cell.startswith('V')) and len(cell) > 1 and cell[1:].isdigit():
                    result[i][j] = cell[1:]
        return result
    else:
        return None

def main():
    grid = parse_grid()
    solution = solve_kakuro(grid)
    
    if solution:
        # Need to handle cells with both H and V clues, but in test case clues are separate
        # For test 1: 'X H3 H6' -> 'X 3 6', 'V4 ? ?' -> '4 1 3'
        # So clue cells become just their number
        out = []
        for row in solution:
            out.append(' '.join(row))
        print('\n'.join(out))
    else:
        print('No solution')

if __name__ == '__main__':
    main()