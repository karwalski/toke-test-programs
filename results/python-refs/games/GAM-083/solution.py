import sys

def solve_arrow_maze():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    if not lines:
        return
    
    grid = lines
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Find start position
    start_pos = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start_pos = (r, c)
                break
        if start_pos:
            break
    
    if not start_pos:
        return
    
    # Direction mappings
    directions = {
        '^': (-1, 0),
        'v': (1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }
    
    visited = set()
    r, c = start_pos
    steps = 0
    
    while True:
        # Check if we've been here before (loop)
        if (r, c) in visited:
            print("Loop detected")
            return
        
        visited.add((r, c))
        
        # Check if we reached the exit
        if grid[r][c] == 'E':
            print(steps)
            return
        
        # Get the arrow direction (skip if it's S)
        if grid[r][c] == 'S':
            # Look for the first non-S adjacent cell with an arrow
            found_next = False
            for dr, dc in directions.values():
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] in directions:
                    r, c = nr, nc
                    steps += 1
                    found_next = True
                    break
            if not found_next:
                print("Out of bounds")
                return
            continue
        
        # Follow the arrow
        if grid[r][c] not in directions:
            print("Out of bounds")
            return
            
        dr, dc = directions[grid[r][c]]
        r += dr
        c += dc
        steps += 1
        
        # Check bounds
        if not (0 <= r < rows and 0 <= c < cols):
            print("Out of bounds")
            return

solve_arrow_maze()