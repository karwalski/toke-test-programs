def get_knight_moves(row, col, n):
    """Get all valid knight moves from position (row, col) on an n×n board"""
    moves = []
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for dr, dc in knight_moves:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < n and 0 <= new_col < n:
            moves.append((new_row, new_col))
    
    return moves

def count_accessible_moves(row, col, n, board):
    """Count how many unvisited squares can be reached from (row, col)"""
    if board[row][col] != 0:  # Already visited
        return 0
    
    count = 0
    for next_row, next_col in get_knight_moves(row, col, n):
        if board[next_row][next_col] == 0:  # Unvisited
            count += 1
    
    return count

def solve_knight_tour(n, start_row, start_col):
    """Solve knight's tour using Warnsdorff's heuristic"""
    board = [[0 for _ in range(n)] for _ in range(n)]
    
    # Start from the given position
    row, col = start_row, start_col
    board[row][col] = 1
    move_count = 1
    
    while move_count < n * n:
        # Get all possible moves
        possible_moves = get_knight_moves(row, col, n)
        
        # Filter out already visited squares
        valid_moves = [(r, c) for r, c in possible_moves if board[r][c] == 0]
        
        if not valid_moves:
            return None  # No valid moves, tour failed
        
        # Apply Warnsdorff's heuristic: choose the square with fewest onward moves
        best_move = None
        min_degree = float('inf')
        
        for next_row, next_col in valid_moves:
            degree = count_accessible_moves(next_row, next_col, n, board)
            if degree < min_degree:
                min_degree = degree
                best_move = (next_row, next_col)
        
        # Move to the best square
        row, col = best_move
        move_count += 1
        board[row][col] = move_count
    
    return board

def format_output(board):
    """Format the board output to match expected format"""
    if board is None:
        return "No tour found"
    
    n = len(board)
    result = []
    
    for row in board:
        row_str = ""
        for i, val in enumerate(row):
            if i > 0:
                row_str += " "
            row_str += f"{val:2d}"
        result.append(row_str)
    
    return "\n".join(result)

# Read input
line = input().strip()
parts = line.split()
n = int(parts[0])
start_row = int(parts[1])
start_col = int(parts[2])

# Solve the knight's tour
solution = solve_knight_tour(n, start_row, start_col)

# Output the result
print(format_output(solution))