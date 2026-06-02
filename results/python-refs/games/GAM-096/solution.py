import sys

def read_board():
    board = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            board.append(list(line))
    return board

def is_valid_position(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        return board[row][col] != 'X'
    return False

def can_jump(board, from_row, from_col, to_row, to_col):
    # Check if positions are valid
    if not is_valid_position(board, from_row, from_col):
        return False
    if not is_valid_position(board, to_row, to_col):
        return False
    
    # Check if from has a peg and to is empty
    if board[from_row][from_col] != 'O' or board[to_row][to_col] != '.':
        return False
    
    # Check if it's exactly 2 cells away horizontally or vertically
    dr = to_row - from_row
    dc = to_col - from_col
    
    if abs(dr) == 2 and dc == 0:
        # Vertical jump
        mid_row = from_row + dr // 2
        return board[mid_row][from_col] == 'O'
    elif abs(dc) == 2 and dr == 0:
        # Horizontal jump
        mid_col = from_col + dc // 2
        return board[from_row][mid_col] == 'O'
    
    return False

def make_jump(board, from_row, from_col, to_row, to_col):
    dr = to_row - from_row
    dc = to_col - from_col
    
    # Remove peg from source
    board[from_row][from_col] = '.'
    
    # Remove jumped peg
    mid_row = from_row + dr // 2
    mid_col = from_col + dc // 2
    board[mid_row][mid_col] = '.'
    
    # Place peg at destination
    board[to_row][to_col] = 'O'

def undo_jump(board, from_row, from_col, to_row, to_col):
    dr = to_row - from_row
    dc = to_col - from_col
    
    # Remove peg from destination
    board[to_row][to_col] = '.'
    
    # Restore jumped peg
    mid_row = from_row + dr // 2
    mid_col = from_col + dc // 2
    board[mid_row][mid_col] = 'O'
    
    # Place peg back at source
    board[from_row][from_col] = 'O'

def count_pegs(board):
    count = 0
    for row in board:
        for cell in row:
            if cell == 'O':
                count += 1
    return count

def find_center(board):
    return len(board) // 2, len(board[0]) // 2

def is_solved(board):
    center_row, center_col = find_center(board)
    if board[center_row][center_col] != 'O':
        return False
    
    peg_count = 0
    for row in board:
        for cell in row:
            if cell == 'O':
                peg_count += 1
    
    return peg_count == 1

def get_possible_jumps(board):
    jumps = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == 'O':
                # Try all four directions (up, down, left, right)
                directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
                for dr, dc in directions:
                    to_row, to_col = row + dr, col + dc
                    if can_jump(board, row, col, to_row, to_col):
                        jumps.append((row, col, to_row, to_col))
    return jumps

def solve_recursive(board, moves, max_depth):
    if len(moves) > max_depth:
        return None
    
    if is_solved(board):
        return moves[:]
    
    possible_jumps = get_possible_jumps(board)
    
    for from_row, from_col, to_row, to_col in possible_jumps:
        make_jump(board, from_row, from_col, to_row, to_col)
        moves.append((from_row, from_col, to_row, to_col))
        
        result = solve_recursive(board, moves, max_depth)
        if result is not None:
            return result
        
        moves.pop()
        undo_jump(board, from_row, from_col, to_row, to_col)
    
    return None

def solve_board(board):
    initial_pegs = count_pegs(board)
    max_depth = initial_pegs - 1
    
    solution = solve_recursive(board, [], max_depth)
    return solution

def main():
    board = read_board()
    solution = solve_board(board)
    
    if solution is None:
        print("No solution")
    else:
        for from_row, from_col, to_row, to_col in solution:
            print(f"{from_row},{from_col} to {to_row},{to_col}")

if __name__ == "__main__":
    main()