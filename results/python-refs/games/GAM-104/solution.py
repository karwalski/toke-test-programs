from collections import deque

def parse_input():
    lines = []
    while True:
        try:
            line = input().strip()
            if line:
                lines.append(line)
        except EOFError:
            break
    
    board_size = int(lines[0])
    player1_pos = tuple(map(int, lines[1].split()))
    player2_pos = tuple(map(int, lines[2].split()))
    
    walls = []
    for i in range(3, len(lines)):
        parts = lines[i].split()
        orientation = parts[0]
        row = int(parts[1])
        col = int(parts[2])
        walls.append((orientation, row, col))
    
    return board_size, player1_pos, player2_pos, walls

def can_move(from_pos, to_pos, walls, board_size):
    from_row, from_col = from_pos
    to_row, to_col = to_pos
    
    # Check if destination is within bounds
    if to_row < 0 or to_row >= board_size or to_col < 0 or to_col >= board_size:
        return False
    
    # Check if movement is only one step in cardinal direction
    if abs(from_row - to_row) + abs(from_col - to_col) != 1:
        return False
    
    # Check for walls blocking the movement
    for orientation, wall_row, wall_col in walls:
        if orientation == 'H':
            # Horizontal wall blocks vertical movement
            if from_col == to_col and wall_col <= from_col <= wall_col + 1:
                if (from_row == wall_row and to_row == wall_row + 1) or \
                   (from_row == wall_row + 1 and to_row == wall_row):
                    return False
        else:  # orientation == 'V'
            # Vertical wall blocks horizontal movement
            if from_row == to_row and wall_row <= from_row <= wall_row + 1:
                if (from_col == wall_col and to_col == wall_col + 1) or \
                   (from_col == wall_col + 1 and to_col == wall_col):
                    return False
    
    return True

def has_path_to_goal(start_pos, goal_row, walls, board_size):
    queue = deque([start_pos])
    visited = {start_pos}
    
    while queue:
        current_pos = queue.popleft()
        current_row, current_col = current_pos
        
        # Check if reached goal row
        if current_row == goal_row:
            return True
        
        # Try all four directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            next_pos = (current_row + dr, current_col + dc)
            
            if next_pos not in visited and can_move(current_pos, next_pos, walls, board_size):
                visited.add(next_pos)
                queue.append(next_pos)
    
    return False

def solve():
    board_size, player1_pos, player2_pos, walls = parse_input()
    
    # Player 1 starts at row 0, goal is row 8 (board_size - 1)
    # Player 2 starts at row 8, goal is row 0
    player1_goal = board_size - 1
    player2_goal = 0
    
    player1_has_path = has_path_to_goal(player1_pos, player1_goal, walls, board_size)
    player2_has_path = has_path_to_goal(player2_pos, player2_goal, walls, board_size)
    
    if player1_has_path and player2_has_path:
        print("Both paths exist")
    elif not player1_has_path:
        print("Player 1 blocked")
    else:
        print("Player 2 blocked")

solve()