import random

def generate_minesweeper_board(rows, cols, mines, seed):
    # Set the random seed
    random.seed(seed)
    
    # Create empty board
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Generate mine positions
    positions = [(r, c) for r in range(rows) for c in range(cols)]
    mine_positions = random.sample(positions, mines)
    
    # Place mines
    for r, c in mine_positions:
        board[r][c] = 'M'
    
    # Calculate numbers for non-mine cells
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != 'M':
                count = 0
                # Check all 8 adjacent cells
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'M':
                            count += 1
                board[r][c] = count
    
    return board

def print_board(board):
    for row in board:
        print(''.join(str(cell) for cell in row))

# Read input
line = input().strip()
rows, cols, mines, seed = map(int, line.split())

# Generate and display board
board = generate_minesweeper_board(rows, cols, mines, seed)
print_board(board)