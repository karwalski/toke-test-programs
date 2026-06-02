import sys

def check_winner(board):
    rows = len(board)
    cols = len(board[0])
    
    # Check horizontal
    for r in range(rows):
        for c in range(cols - 3):
            if board[r][c] != '.' and board[r][c] == board[r][c+1] == board[r][c+2] == board[r][c+3]:
                return board[r][c]
    
    # Check vertical
    for r in range(rows - 3):
        for c in range(cols):
            if board[r][c] != '.' and board[r][c] == board[r+1][c] == board[r+2][c] == board[r+3][c]:
                return board[r][c]
    
    # Check diagonal (top-left to bottom-right)
    for r in range(rows - 3):
        for c in range(cols - 3):
            if board[r][c] != '.' and board[r][c] == board[r+1][c+1] == board[r+2][c+2] == board[r+3][c+3]:
                return board[r][c]
    
    # Check diagonal (top-right to bottom-left)
    for r in range(rows - 3):
        for c in range(3, cols):
            if board[r][c] != '.' and board[r][c] == board[r+1][c-1] == board[r+2][c-2] == board[r+3][c-3]:
                return board[r][c]
    
    return None

# Read input
board = []
for _ in range(6):
    line = input().strip()
    board.append(line)

# Check for winner
winner = check_winner(board)

if winner == 'R':
    print('R wins')
elif winner == 'Y':
    print('Y wins')
else:
    print('No winner')