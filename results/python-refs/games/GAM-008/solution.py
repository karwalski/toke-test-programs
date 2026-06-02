def get_knight_moves(pos):
    file, rank = pos[0], int(pos[1])
    file_num = ord(file) - ord('a')
    
    moves = []
    knight_offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for df, dr in knight_offsets:
        new_file = file_num + df
        new_rank = rank + dr
        
        if 0 <= new_file <= 7 and 1 <= new_rank <= 8:
            moves.append(chr(ord('a') + new_file) + str(new_rank))
    
    return moves

def get_king_moves(pos):
    file, rank = pos[0], int(pos[1])
    file_num = ord(file) - ord('a')
    
    moves = []
    king_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    
    for df, dr in king_offsets:
        new_file = file_num + df
        new_rank = rank + dr
        
        if 0 <= new_file <= 7 and 1 <= new_rank <= 8:
            moves.append(chr(ord('a') + new_file) + str(new_rank))
    
    return moves

def get_queen_moves(pos):
    return get_rook_moves(pos) + get_bishop_moves(pos)

def get_rook_moves(pos):
    file, rank = pos[0], int(pos[1])
    file_num = ord(file) - ord('a')
    
    moves = []
    
    # Horizontal moves
    for f in range(8):
        if f != file_num:
            moves.append(chr(ord('a') + f) + str(rank))
    
    # Vertical moves
    for r in range(1, 9):
        if r != rank:
            moves.append(file + str(r))
    
    return moves

def get_bishop_moves(pos):
    file, rank = pos[0], int(pos[1])
    file_num = ord(file) - ord('a')
    
    moves = []
    
    # Diagonal moves
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    
    for df, dr in directions:
        for i in range(1, 8):
            new_file = file_num + i * df
            new_rank = rank + i * dr
            
            if 0 <= new_file <= 7 and 1 <= new_rank <= 8:
                moves.append(chr(ord('a') + new_file) + str(new_rank))
            else:
                break
    
    return moves

def get_pawn_moves(pos):
    file, rank = pos[0], int(pos[1])
    
    moves = []
    
    # Pawn moves forward (assuming white pawn, moving up)
    if rank < 8:
        moves.append(file + str(rank + 1))
    
    # Initial two-square move
    if rank == 2 and rank + 2 <= 8:
        moves.append(file + str(rank + 2))
    
    return moves

def solve_chess_moves():
    line = input().strip()
    piece, position = line.split()
    
    if piece == 'N':
        moves = get_knight_moves(position)
    elif piece == 'K':
        moves = get_king_moves(position)
    elif piece == 'Q':
        moves = get_queen_moves(position)
    elif piece == 'R':
        moves = get_rook_moves(position)
    elif piece == 'B':
        moves = get_bishop_moves(position)
    elif piece == 'P':
        moves = get_pawn_moves(position)
    
    moves.sort()
    for move in moves:
        print(move)

solve_chess_moves()