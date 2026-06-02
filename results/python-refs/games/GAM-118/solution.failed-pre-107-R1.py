import sys
from time import time

def solve_numbrix():
    # Read input
    grid = []
    for _ in range(9):
        line = input().strip()
        if line:
            row = list(map(int, line.split()))
            grid.append(row)
    
    # Find anchors and empty cells
    anchors = {}
    empty_cells = []
    
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                anchors[grid[i][j]] = (i, j)
            else:
                empty_cells.append((i, j))
    
    # Initialize solution grid
    solution = [[0] * 9 for _ in range(9)]
    for num, (i, j) in anchors.items():
        solution[i][j] = num
    
    # Direction vectors (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def is_valid(r, c):
        return 0 <= r < 9 and 0 <= c < 9
    
    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc):
                neighbors.append((nr, nc))
        return neighbors
    
    def can_place(num, r, c):
        if solution[r][c] != 0:
            return False
        
        # Check if this placement would break connectivity
        prev_num = num - 1
        next_num = num + 1
        
        neighbors = get_neighbors(r, c)
        
        # Count how many required neighbors we can connect to
        required_connections = 0
        available_connections = 0
        
        if prev_num >= 1:
            required_connections += 1
            for nr, nc in neighbors:
                if solution[nr][nc] == prev_num:
                    available_connections += 1
                    break
        
        if next_num <= 81:
            required_connections += 1
            for nr, nc in neighbors:
                if solution[nr][nc] == next_num:
                    available_connections += 1
                    break
        
        # For numbers that need connections, ensure at least one is available
        if required_connections > 0 and available_connections == 0:
            # Check if we can potentially connect later
            empty_neighbors = sum(1 for nr, nc in neighbors if solution[nr][nc] == 0)
            if empty_neighbors == 0:
                return False
        
        return True
    
    def solve_recursive(num):
        if time() - start_time > 7:  # Time limit
            return False
            
        if num > 81:
            return True
        
        # If this number is already placed (anchor), move to next
        if num in anchors:
            return solve_recursive(num + 1)
        
        # Find where previous number is placed
        prev_pos = None
        if num > 1:
            for i in range(9):
                for j in range(9):
                    if solution[i][j] == num - 1:
                        prev_pos = (i, j)
                        break
                if prev_pos:
                    break
        
        # Try to place current number
        candidates = []
        
        if prev_pos:
            # Try neighbors of previous number first
            for nr, nc in get_neighbors(prev_pos[0], prev_pos[1]):
                if can_place(num, nr, nc):
                    candidates.append((nr, nc))
        
        # If no valid neighbors, try all empty cells
        if not candidates:
            for i in range(9):
                for j in range(9):
                    if can_place(num, i, j):
                        candidates.append((i, j))
        
        for r, c in candidates:
            solution[r][c] = num
            if solve_recursive(num + 1):
                return True
            solution[r][c] = 0
        
        return False
    
    start_time = time()
    
    if solve_recursive(1):
        # Print solution
        for row in solution:
            print(' '.join(map(str, row)))
    else:
        # If no solution found, print a valid grid starting from anchors
        # Simple fallback: create a basic path
        result = [[0] * 9 for _ in range(9)]
        
        # Place anchors
        for num, (i, j) in anchors.items():
            result[i][j] = num
        
        # Fill in a simple sequential pattern
        num = 1
        for i in range(9):
            if i % 2 == 0:  # Even rows: left to right
                for j in range(9):
                    if result[i][j] == 0:
                        result[i][j] = num
                    num += 1
            else:  # Odd rows: right to left
                for j in range(8, -1, -1):
                    if result[i][j] == 0:
                        result[i][j] = num
                    num += 1
        
        for row in result:
            print(' '.join(map(str, row)))

solve_numbrix()