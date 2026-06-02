def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '.':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '.':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '.':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '.':
        return board[0][2]
    
    return None

def is_board_full(board):
    for row in board:
        for cell in row:
            if cell == '.':
                return False
    return True

def minimax(board, is_maximizing, player, opponent):
    winner = check_winner(board)
    
    if winner == player:
        return 1
    elif winner == opponent:
        return -1
    elif is_board_full(board):
        return 0
    
    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    board[i][j] = player
                    score = minimax(board, False, player, opponent)
                    board[i][j] = '.'
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '.':
                    board[i][j] = opponent
                    score = minimax(board, True, player, opponent)
                    board[i][j] = '.'
                    best_score = min(score, best_score)
        return best_score

def get_best_move(board, player):
    opponent = 'X' if player == 'O' else 'O'
    best_score = -float('inf')
    best_move = None
    
    for i in range(3):
        for j in range(3):
            if board[i][j] == '.':
                board[i][j] = player
                score = minimax(board, False, player, opponent)
                board[i][j] = '.'
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    return best_move

# Read input
board = []
for _ in range(3):
    board.append(list(input().strip()))

player = input().strip()

# Get best move
best_move = get_best_move(board, player)
print(f"{best_move[0]} {best_move[1]}")