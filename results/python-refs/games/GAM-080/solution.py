from collections import deque

def solve():
    n = int(input().strip())
    grid = []
    for _ in range(n):
        grid.append(input().strip())
    
    command = input().strip()  # "find"
    
    # Find caterpillar head, body segments, and food positions
    head = None
    body = []
    food = []
    
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 'H':
                head = (i, j)
            elif grid[i][j] == 'B':
                body.append((i, j))
            elif grid[i][j] == 'F':
                food.append((i, j))
    
    # Sort body segments to maintain order (assume they form a connected sequence)
    # Start from head and trace the body
    if body:
        ordered_body = []
        current = head
        remaining_body = set(body)
        
        while remaining_body:
            # Find adjacent body segment
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = current[0] + di, current[1] + dj
                if (ni, nj) in remaining_body:
                    ordered_body.append((ni, nj))
                    remaining_body.remove((ni, nj))
                    current = (ni, nj)
                    break
        body = ordered_body
    
    # BFS to find shortest path to eat all food
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # U, D, L, R
    dir_chars = ['U', 'D', 'L', 'R']
    
    # State: (head_pos, body_positions_tuple, food_eaten_bitmask)
    food_set = set(food)
    initial_food_mask = 0
    
    # Check if head starts on food
    if head in food_set:
        initial_food_mask |= (1 << food.index(head))
    
    queue = deque([(head, tuple(body), initial_food_mask, "")])
    visited = set()
    visited.add((head, tuple(body), initial_food_mask))
    
    target_mask = (1 << len(food)) - 1  # All food eaten
    
    while queue:
        curr_head, curr_body, food_mask, path = queue.popleft()
        
        if food_mask == target_mask:
            print(path)
            return
        
        for i, (di, dj) in enumerate(directions):
            new_head = (curr_head[0] + di, curr_head[1] + dj)
            
            # Check bounds
            if not (0 <= new_head[0] < n and 0 <= new_head[1] < n):
                continue
            
            # Check if new head position collides with body
            if new_head in curr_body:
                continue
            
            # Move body (head becomes first body segment, last body segment is removed)
            new_body = list(curr_body)
            if new_body:
                new_body = [curr_head] + new_body[:-1]
            else:
                new_body = [curr_head] if curr_body or len(path) > 0 else []
            
            # Check if head eats food
            new_food_mask = food_mask
            if new_head in food_set:
                food_idx = food.index(new_head)
                new_food_mask |= (1 << food_idx)
            
            state = (new_head, tuple(new_body), new_food_mask)
            if state not in visited:
                visited.add(state)
                queue.append((new_head, tuple(new_body), new_food_mask, path + dir_chars[i]))
    
    print("No solution")

solve()