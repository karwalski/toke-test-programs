import random

def solve():
    seed = int(input().strip())
    random.seed(seed)
    
    # Initialize 10x10 grid
    grid = [['.' for _ in range(10)] for _ in range(10)]
    
    # Ship definitions based on expected output
    ships = [
        ('C', 5),  # Carrier
        ('B', 6),  # Battleship (appears to be 6 in example)
        ('D', 3),  # Destroyer
        ('S', 4)   # Submarine
    ]
    
    def can_place_ship(grid, row, col, length, direction):
        # Check bounds first
        if direction == 'H':  # Horizontal
            if col + length > 10 or row >= 10 or row < 0 or col < 0:
                return False
            for i in range(length):
                if col + i >= 10 or grid[row][col + i] != '.':
                    return False
            # Check adjacent cells for spacing
            for i in range(max(0, col-1), min(10, col+length+1)):
                if i >= 10:
                    break
                if row > 0 and grid[row-1][i] != '.':
                    return False
                if row < 9 and grid[row+1][i] != '.':
                    return False
            if col > 0 and grid[row][col-1] != '.':
                return False
            if col + length < 10 and grid[row][col+length] != '.':
                return False
        else:  # Vertical
            if row + length > 10 or row < 0 or col >= 10 or col < 0:
                return False
            for i in range(length):
                if row + i >= 10 or grid[row + i][col] != '.':
                    return False
            # Check adjacent cells for spacing
            for i in range(max(0, row-1), min(10, row+length+1)):
                if i >= 10:
                    break
                if col > 0 and grid[i][col-1] != '.':
                    return False
                if col < 9 and grid[i][col+1] != '.':
                    return False
            if row > 0 and grid[row-1][col] != '.':
                return False
            if row + length < 10 and grid[row+length][col] != '.':
                return False
        return True
    
    def place_ship(grid, row, col, length, direction, ship_char):
        if direction == 'H':
            for i in range(length):
                if col + i < 10 and row < 10:
                    grid[row][col + i] = ship_char
        else:
            for i in range(length):
                if row + i < 10 and col < 10:
                    grid[row + i][col] = ship_char
    
    # Place ships with multiple attempts
    for ship_char, length in ships:
        placed = False
        attempts = 0
        max_attempts = 1000
        
        while not placed and attempts < max_attempts:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            direction = random.choice(['H', 'V'])
            
            if can_place_ship(grid, row, col, length, direction):
                place_ship(grid, row, col, length, direction, ship_char)
                placed = True
            
            attempts += 1
        
        if not placed:
            # If we can't place with random, try systematic placement
            for r in range(10):
                for c in range(10):
                    for d in ['H', 'V']:
                        if can_place_ship(grid, r, c, length, d):
                            place_ship(grid, r, c, length, d, ship_char)
                            placed = True
                            break
                    if placed:
                        break
                if placed:
                    break
    
    # Print grid
    for row in grid:
        print(''.join(row))

solve()