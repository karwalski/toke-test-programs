import sys

def solve():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Parse grid size
    grid_size = int(lines[0])
    
    # Parse food positions
    food_positions = set()
    i = 1
    while i < len(lines) and lines[i].strip():
        parts = lines[i].split()
        if len(parts) == 2:
            food_positions.add((int(parts[0]), int(parts[1])))
        i += 1
    
    # Find move sequence (after blank line)
    moves = ""
    for j in range(i, len(lines)):
        if lines[j].strip():
            moves = lines[j]
            break
    
    # Initialize snake at position (0, 0)
    snake = [(0, 0)]
    score = 0
    
    # Direction mappings
    directions = {
        'U': (-1, 0),
        'D': (1, 0),
        'L': (0, -1),
        'R': (0, 1)
    }
    
    # Process each move
    for move in moves:
        if move not in directions:
            continue
            
        dr, dc = directions[move]
        head_r, head_c = snake[0]
        new_head = (head_r + dr, head_c + dc)
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= grid_size or 
            new_head[1] < 0 or new_head[1] >= grid_size):
            print(f"{score} Game Over")
            return
        
        # Check self collision
        if new_head in snake:
            print(f"{score} Game Over")
            return
        
        # Add new head
        snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head in food_positions:
            score += 1
            food_positions.remove(new_head)
        else:
            # Remove tail if no food eaten
            snake.pop()
    
    print(f"{score} Alive")

solve()