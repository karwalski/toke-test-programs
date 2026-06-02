import sys
from itertools import combinations

def parse_grid():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip())
    
    grid = []
    for line in lines:
        grid.append(line.split())
    
    return grid

def solve_kakuro(grid):
    rows = len(grid)
    cols = len(grid[0])
    
    # Find empty cells and clues
    empty_cells = []
    h_clues = {}  # (row, col) -> sum
    v_clues = {}  # (row, col) -> sum
    
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            if cell == '?':
                empty_cells.append((i, j))
            elif cell.startswith('H'):
                h_clues[(i, j)] = int(cell[1:])
            elif cell.startswith('V'):
                v_clues[(i, j)] = int(cell[1:])
    
    # Build segments for each clue
    h_segments = {}
    v_segments = {}
    
    # Horizontal segments
    for (r, c), target_sum in h_clues.items():
        segment = []
        for j in range(c + 1, cols):
            if grid[r][j] == '?':
                segment.append((r, j))
            else:
                break
        if segment:
            h_segments[(r, c)] = (target_sum, segment)
    
    # Vertical segments
    for (r, c), target_sum in v_clues.items():
        segment = []
        for i in range(r + 1, rows):
            if grid[i][c] == '?':
                segment.append((i, c))
            else:
                break
        if segment:
            v_segments[(r, c)] = (target_sum, segment)
    
    # Create assignment array
    assignment = {}
    
    def is_valid():
        # Check horizontal constraints
        for (target_sum, segment) in h_segments.values():
            if all(cell in assignment for cell in segment):
                values = [assignment[cell] for cell in segment]
                if sum(values) != target_sum or len(set(values)) != len(values):
                    return False
        
        # Check vertical constraints
        for (target_sum, segment) in v_segments.values():
            if all(cell in assignment for cell in segment):
                values = [assignment[cell] for cell in segment]
                if sum(values) != target_sum or len(set(values)) != len(values):
                    return False
        
        return True
    
    def can_complete():
        # Check if partial assignment can lead to valid solution
        for (target_sum, segment) in h_segments.values():
            assigned = [assignment[cell] for cell in segment if cell in assignment]
            unassigned_count = len(segment) - len(assigned)
            
            if assigned:
                current_sum = sum(assigned)
                remaining_sum = target_sum - current_sum
                
                if remaining_sum <= 0:
                    return False
                
                if unassigned_count > 0:
                    # Check if remaining sum can be achieved
                    used_digits = set(assigned)
                    available_digits = [d for d in range(1, 10) if d not in used_digits]
                    
                    if len(available_digits) < unassigned_count:
                        return False
                    
                    min_possible = sum(sorted(available_digits)[:unassigned_count])
                    max_possible = sum(sorted(available_digits)[-unassigned_count:])
                    
                    if remaining_sum < min_possible or remaining_sum > max_possible:
                        return False
        
        # Same check for vertical segments
        for (target_sum, segment) in v_segments.values():
            assigned = [assignment[cell] for cell in segment if cell in assignment]
            unassigned_count = len(segment) - len(assigned)
            
            if assigned:
                current_sum = sum(assigned)
                remaining_sum = target_sum - current_sum
                
                if remaining_sum <= 0:
                    return False
                
                if unassigned_count > 0:
                    used_digits = set(assigned)
                    available_digits = [d for d in range(1, 10) if d not in used_digits]
                    
                    if len(available_digits) < unassigned_count:
                        return False
                    
                    min_possible = sum(sorted(available_digits)[:unassigned_count])
                    max_possible = sum(sorted(available_digits)[-unassigned_count:])
                    
                    if remaining_sum < min_possible or remaining_sum > max_possible:
                        return False
        
        return True
    
    def backtrack(cell_idx):
        if cell_idx == len(empty_cells):
            return is_valid()
        
        cell = empty_cells[cell_idx]
        
        for digit in range(1, 10):
            assignment[cell] = digit
            
            if can_complete():
                if backtrack(cell_idx + 1):
                    return True
            
            del assignment[cell]
        
        return False
    
    if backtrack(0):
        # Fill the grid with solution
        for (r, c), value in assignment.items():
            grid[r][c] = str(value)
        return grid
    else:
        return None

def main():
    grid = parse_grid()
    solution = solve_kakuro(grid)
    
    if solution:
        for row in solution:
            print(' '.join(row))
    else:
        print('No solution')

if __name__ == '__main__':
    main()