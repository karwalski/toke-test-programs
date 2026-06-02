import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates grid from moves
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    if blank_line_idx == -1:
        # No blank line found, assume all lines are grid
        grid_lines = lines
        move_lines = []
    else:
        grid_lines = lines[:blank_line_idx]
        move_lines = lines[blank_line_idx + 1:]
    
    # Parse grid
    grid = []
    for line in grid_lines:
        if line:  # Skip empty lines
            grid.append(list(line))
    
    # Parse moves
    moves = []
    for line in move_lines:
        if line.strip():
            parts = line.split()
            if len(parts) >= 2:
                pos_part = parts[0].rstrip(',')
                direction = parts[1]
                row, col = map(int, pos_part.split(','))
                moves.append((row, col, direction))
    
    return grid, moves

def is_valid_position(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def get_direction_offset(direction):
    if direction == "right":
        return (0, 1)
    elif direction == "left":
        return (0, -1)
    elif direction == "up":
        return (-1, 0)
    elif direction == "down":
        return (1, 0)
    else:
        return None

def make_move(grid, start_row, start_col, direction):
    # Get direction offset
    offset = get_direction_offset(direction)
    if offset is None:
        return False
    
    dr, dc = offset
    
    # Calculate positions
    middle_row = start_row + dr
    middle_col = start_col + dc
    end_row = start_row + 2 * dr
    end_col = start_col + 2 * dc
    
    # Check if all positions are valid
    if not (is_valid_position(grid, start_row, start_col) and
            is_valid_position(grid, middle_row, middle_col) and
            is_valid_position(grid, end_row, end_col)):
        return False
    
    # Check if move is valid: start has peg, middle has peg, end is empty
    if (grid[start_row][start_col] == 'O' and
        grid[middle_row][middle_col] == 'O' and
        grid[end_row][end_col] == '.'):
        
        # Make the move
        grid[start_row][start_col] = '.'
        grid[middle_row][middle_col] = '.'
        grid[end_row][end_col] = 'O'
        return True
    
    return False

def solve():
    grid, moves = read_input()
    
    for i, (row, col, direction) in enumerate(moves):
        if not make_move(grid, row, col, direction):
            print(f"Invalid move at step {i + 1}")
            return
    
    print("Valid")

solve()