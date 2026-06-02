import sys
from itertools import product

def parse_board():
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            lines.append(line)
    return lines

def get_neighbors(row, col, rows, cols):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def solve_minesweeper(board):
    rows = len(board)
    cols = len(board[0])
    
    # Find all unrevealed cells
    unrevealed = []
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == '?':
                unrevealed.append((r, c))
    
    if not unrevealed:
        return []
    
    # Generate all possible mine configurations
    n_unrevealed = len(unrevealed)
    deductions = []
    valid_configs = []
    
    # Try all possible mine assignments to unrevealed cells
    for config in product([0, 1], repeat=n_unrevealed):
        # Create a test board with this configuration
        test_board = [list(row) for row in board]
        for i, (r, c) in enumerate(unrevealed):
            if config[i] == 1:
                test_board[r][c] = 'M'
            else:
                test_board[r][c] = 'S'  # Safe
        
        # Check if this configuration is valid
        valid = True
        for r in range(rows):
            for c in range(cols):
                if test_board[r][c].isdigit():
                    target_count = int(test_board[r][c])
                    neighbors = get_neighbors(r, c, rows, cols)
                    mine_count = 0
                    for nr, nc in neighbors:
                        if test_board[nr][nc] == 'M':
                            mine_count += 1
                    if mine_count != target_count:
                        valid = False
                        break
            if not valid:
                break
        
        if valid:
            valid_configs.append(config)
    
    if not valid_configs:
        return []
    
    # Find cells that have the same value in all valid configurations
    for i, (r, c) in enumerate(unrevealed):
        values = [config[i] for config in valid_configs]
        if all(v == 0 for v in values):
            deductions.append(f"SAFE {r} {c}")
        elif all(v == 1 for v in values):
            deductions.append(f"MINE {r} {c}")
    
    return deductions

def main():
    board = parse_board()
    deductions = solve_minesweeper(board)
    
    if deductions:
        for deduction in deductions:
            print(deduction)
    else:
        print("No deductions")

if __name__ == "__main__":
    main()