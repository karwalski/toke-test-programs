def evaluate_material_balance(fen_pieces):
    # Piece values
    piece_values = {
        'p': -1,  # black pawn
        'r': -5,  # black rook
        'n': -3,  # black knight
        'b': -3,  # black bishop
        'q': -9,  # black queen
        'k': 0,   # black king (no material value)
        'P': 1,   # white pawn
        'R': 5,   # white rook
        'N': 3,   # white knight
        'B': 3,   # white bishop
        'Q': 9,   # white queen
        'K': 0    # white king (no material value)
    }
    
    score = 0
    for char in fen_pieces:
        if char in piece_values:
            score += piece_values[char]
    
    return score

# Read input from stdin
fen_input = input().strip()
result = evaluate_material_balance(fen_input)
print(result)