def read_input():
    board = []
    for _ in range(8):
        board.append(list(input().strip()))
    player = input().strip()
    move_line = input().strip().split()
    row, col = int(move_line[0]), int(move_line[1])
    return board, player, row, col

def is_valid_move(board, player, row, col):
    if board[row][col] != '.':
        return False
    
    opponent = 'W' if player == 'B' else 'B'
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []
        
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc
        
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player and pieces_to_flip:
            return True
    
    return False

def make_move(board, player, row, col):
    if not is_valid_move(board, player, row, col):
        return None
    
    new_board = [row[:] for row in board]
    new_board[row][col] = player
    
    opponent = 'W' if player == 'B' else 'B'
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        pieces_to_flip = []
        
        while 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] == opponent:
            pieces_to_flip.append((r, c))
            r += dr
            c += dc
        
        if 0 <= r < 8 and 0 <= c < 8 and new_board[r][c] == player and pieces_to_flip:
            for flip_r, flip_c in pieces_to_flip:
                new_board[flip_r][flip_c] = player
    
    return new_board

def print_board(board):
    for row in board:
        print(''.join(row))

def main():
    board, player, row, col = read_input()
    
    result_board = make_move(board, player, row, col)
    
    if result_board is None:
        print("Invalid move")
    else:
        print_board(result_board)

if __name__ == "__main__":
    main()