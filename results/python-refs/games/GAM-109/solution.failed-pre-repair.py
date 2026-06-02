def read_input():
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    
    # Parse board
    board = []
    i = 0
    while i < len(lines) and lines[i] and ('.' in lines[i] or any(c.isalpha() for c in lines[i])):
        board.append(list(lines[i]))
        i += 1
    
    # Parse player color
    if i >= len(lines):
        raise ValueError("Missing player color")
    player_color = lines[i]
    i += 1
    
    # Parse piece shape
    piece = []
    while i < len(lines) and ('X' in lines[i] or '.' in lines[i]):
        piece.append(list(lines[i]))
        i += 1
    
    # Parse placement position
    if i >= len(lines):
        raise ValueError("Missing placement position")
    placement = lines[i].split()
    if len(placement) < 2:
        raise ValueError("Invalid placement format")
    row, col = int(placement[0]), int(placement[1])
    
    return board, player_color, piece, row, col

def validate_placement(board, player_color, piece, start_row, start_col):
    if not board or not board[0]:
        return "Invalid: empty board"
    
    board_height = len(board)
    board_width = len(board[0])
    
    if not piece:
        return "Invalid: empty piece"
    
    piece_height = len(piece)
    piece_width = len(piece[0]) if piece_height > 0 else 0
    
    # Get piece positions
    piece_positions = []
    for r in range(piece_height):
        for c in range(len(piece[r])):
            if piece[r][c] == 'X':
                piece_positions.append((r, c))
    
    if not piece_positions:
        return "Invalid: no piece blocks"
    
    # Check if piece fits on board and get board positions
    board_positions = []
    for pr, pc in piece_positions:
        br, bc = start_row + pr, start_col + pc
        if br < 0 or br >= board_height or bc < 0 or bc >= board_width:
            return "Invalid: out of bounds"
        board_positions.append((br, bc))
    
    # Check for overlaps
    for br, bc in board_positions:
        if board[br][bc] != '.':
            return "Invalid: overlap"
    
    # Check for edge sharing with same color
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for br, bc in board_positions:
        for dr, dc in directions:
            nr, nc = br + dr, bc + dc
            if 0 <= nr < board_height and 0 <= nc < board_width:
                if board[nr][nc] == player_color:
                    return "Invalid: edge sharing"
    
    # Check for corner touching with same color
    corners = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    touches_corner = False
    for br, bc in board_positions:
        for dr, dc in corners:
            nr, nc = br + dr, bc + dc
            if 0 <= nr < board_height and 0 <= nc < board_width:
                if board[nr][nc] == player_color:
                    touches_corner = True
                    break
        if touches_corner:
            break
    
    if not touches_corner:
        return "Invalid: no corner touch"
    
    return "Valid"

def main():
    try:
        board, player_color, piece, row, col = read_input()
        result = validate_placement(board, player_color, piece, row, col)
        print(result)
    except Exception as e:
        print("Invalid: input error")

if __name__ == "__main__":
    main()