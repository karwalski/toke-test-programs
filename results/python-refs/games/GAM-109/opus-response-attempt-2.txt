import sys

def main():
    data = sys.stdin.read().split('\n')
    while data and data[-1] == '':
        data.pop()
    
    if not data:
        print("Invalid: input error")
        return
    
    width = len(data[0])
    board = []
    i = 0
    while i < len(data) and len(data[i]) == width and all(c == '.' or c.isalpha() for c in data[i]):
        board.append(list(data[i]))
        i += 1
    
    if i >= len(data):
        print("Invalid: input error")
        return
    player_color = data[i].strip()
    i += 1
    
    piece = []
    while i < len(data) and data[i] and all(c in 'X.' for c in data[i]):
        piece.append(list(data[i]))
        i += 1
    
    if i >= len(data):
        print("Invalid: input error")
        return
    parts = data[i].split()
    row, col = int(parts[0]), int(parts[1])
    
    board_height = len(board)
    board_width = len(board[0]) if board else 0
    
    piece_positions = []
    for r in range(len(piece)):
        for c in range(len(piece[r])):
            if piece[r][c] == 'X':
                piece_positions.append((r, c))
    
    board_positions = []
    for pr, pc in piece_positions:
        br, bc = row + pr, col + pc
        if br < 0 or br >= board_height or bc < 0 or bc >= board_width:
            print("Invalid: out of bounds")
            return
        board_positions.append((br, bc))
    
    pos_set = set(board_positions)
    
    for br, bc in board_positions:
        if board[br][bc] != '.':
            print("Invalid: overlap")
            return
    
    # Check if board has any existing same-color pieces
    has_existing = any(board[r][c] == player_color for r in range(board_height) for c in range(board_width))
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for br, bc in board_positions:
        for dr, dc in directions:
            nr, nc = br + dr, bc + dc
            if 0 <= nr < board_height and 0 <= nc < board_width:
                if (nr, nc) not in pos_set and board[nr][nc] == player_color:
                    print("Invalid: shares edge with same colour")
                    return
    
    if has_existing:
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
            print("Invalid: no corner touch")
            return
    
    print("Valid")

main()