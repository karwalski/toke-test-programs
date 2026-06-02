def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] in ['X', 'O']:
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] in ['X', 'O']:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] in ['X', 'O']:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] in ['X', 'O']:
        return board[0][2]
    
    return None

# Read input
board = []
for _ in range(3):
    line = input().strip()
    board.append(list(line))

# Check for winner
winner = check_winner(board)

if winner:
    print(f"{winner} wins")
else:
    # Check if board is full (draw) or ongoing
    has_empty = any('.' in row for row in board)
    if has_empty:
        print("Ongoing")
    else:
        print("Draw")