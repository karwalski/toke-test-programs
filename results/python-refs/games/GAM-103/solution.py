import sys
from typing import List, Tuple, Optional

def parse_input() -> List[List[str]]:
    """Parse the triangle input from stdin."""
    lines = []
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line:
            lines.append(list(line))
    return lines

def get_valid_moves(board: List[List[str]]) -> List[Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]]:
    """Get all valid moves in the current board state."""
    moves = []
    rows = len(board)
    
    for r in range(rows):
        for c in range(len(board[r])):
            if board[r][c] == 'O':  # There's a peg here
                # Check all 6 possible directions
                directions = [
                    (-2, 0),   # up
                    (2, 0),    # down
                    (-1, -1),  # up-left
                    (-1, 1),   # up-right
                    (1, -1),   # down-left
                    (1, 1)     # down-right
                ]
                
                for dr, dc in directions:
                    new_r, new_c = r + dr, c + dc
                    mid_r, mid_c = r + dr//2, c + dc//2
                    
                    # Check bounds
                    if (0 <= new_r < rows and 
                        0 <= new_c < len(board[new_r]) and
                        0 <= mid_r < rows and
                        0 <= mid_c < len(board[mid_r])):
                        
                        # Check if move is valid (middle has peg, destination is empty)
                        if (board[mid_r][mid_c] == 'O' and 
                            board[new_r][new_c] == '.'):
                            moves.append(((r, c), (mid_r, mid_c), (new_r, new_c)))
    
    return moves

def make_move(board: List[List[str]], move: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> None:
    """Make a move on the board."""
    (from_r, from_c), (mid_r, mid_c), (to_r, to_c) = move
    board[from_r][from_c] = '.'
    board[mid_r][mid_c] = '.'
    board[to_r][to_c] = 'O'

def undo_move(board: List[List[str]], move: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]) -> None:
    """Undo a move on the board."""
    (from_r, from_c), (mid_r, mid_c), (to_r, to_c) = move
    board[from_r][from_c] = 'O'
    board[mid_r][mid_c] = 'O'
    board[to_r][to_c] = '.'

def count_pegs(board: List[List[str]]) -> int:
    """Count the number of pegs on the board."""
    count = 0
    for row in board:
        for cell in row:
            if cell == 'O':
                count += 1
    return count

def solve(board: List[List[str]], moves_made: List[str]) -> bool:
    """Solve the triangle peg game using backtracking."""
    peg_count = count_pegs(board)
    
    if peg_count == 1:
        return True
    
    valid_moves = get_valid_moves(board)
    
    for move in valid_moves:
        (from_r, from_c), (mid_r, mid_c), (to_r, to_c) = move
        
        # Make the move
        make_move(board, move)
        
        # Format the move string
        move_str = f"peg at {from_r},{from_c} jumps over {mid_r},{mid_c} to {to_r},{to_c}"
        moves_made.append(move_str)
        
        # Recursively try to solve
        if solve(board, moves_made):
            return True
        
        # Backtrack
        moves_made.pop()
        undo_move(board, move)
    
    return False

def main():
    board = parse_input()
    moves_made = []
    
    if solve(board, moves_made):
        for move in moves_made:
            print(move)
    else:
        print("No solution")

if __name__ == "__main__":
    main()