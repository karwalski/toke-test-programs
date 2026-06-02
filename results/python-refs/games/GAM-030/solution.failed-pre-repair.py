import sys

def get_piece_shape(piece_type):
    shapes = {
        'I': [(0,0), (1,0), (2,0), (3,0)],  # vertical line
        'O': [(0,0), (0,1), (1,0), (1,1)],  # square
        'T': [(0,1), (1,0), (1,1), (1,2)],  # T-shape
        'S': [(0,1), (0,2), (1,0), (1,1)],  # S-shape
        'Z': [(0,0), (0,1), (1,1), (1,2)],  # Z-shape
        'J': [(0,0), (1,0), (2,0), (2,1)],  # J-shape
        'L': [(0,1), (1,1), (2,0), (2,1)]   # L-shape
    }
    return shapes[piece_type]

def can_place_piece(board, piece_shape, start_row, start_col):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    for dr, dc in piece_shape:
        r = start_row + dr
        c = start_col + dc
        
        # Check bounds
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        
        # Check collision with existing blocks
        if board[r][c] == 'X':
            return False
    
    return True

def solve():
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line == '':
            break
        lines.append(line)
    
    # Read piece and column
    piece_info = input().strip().split()
    piece_type = piece_info[0]
    column = int(piece_info[1])
    
    board = lines
    piece_shape = get_piece_shape(piece_type)
    
    if not board:
        print("Invalid")
        return
    
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    
    # Check if the piece can fit at the given column at all
    max_col_needed = column + max(dc for dr, dc in piece_shape)
    if max_col_needed >= cols:
        print("Invalid")
        return
    
    # Find the lowest valid row
    for row in range(rows - 1, -1, -1):
        if can_place_piece(board, piece_shape, row, column):
            print(row)
            return
    
    print("Invalid")

solve()