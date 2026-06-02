import random
import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse first line
    parts = lines[0].split()
    rows, cols, seed = int(parts[0]), int(parts[1]), int(parts[2])
    
    # Parse words
    words = []
    for i in range(1, len(lines)):
        if lines[i]:
            words.append(lines[i])
    
    # Set random seed
    random.seed(seed)
    
    # Initialize grid with spaces
    grid = [[' ' for _ in range(cols)] for _ in range(rows)]
    
    # Store word placements
    placements = []
    
    # Try to place each word
    for word in words:
        placed = False
        attempts = 0
        max_attempts = 1000
        
        while not placed and attempts < max_attempts:
            attempts += 1
            
            # Random starting position
            start_row = random.randint(0, rows - 1)
            start_col = random.randint(0, cols - 1)
            
            # Random direction (0=right, 1=down, 2=diagonal down-right, etc.)
            # For simplicity, let's try right first, then down
            directions = [(0, 1), (1, 0)]  # right, down
            direction = random.choice(directions)
            
            dr, dc = direction
            
            # Check if word fits
            end_row = start_row + dr * (len(word) - 1)
            end_col = start_col + dc * (len(word) - 1)
            
            if end_row >= 0 and end_row < rows and end_col >= 0 and end_col < cols:
                # Check if positions are free or have matching letters
                can_place = True
                for i, char in enumerate(word):
                    r = start_row + dr * i
                    c = start_col + dc * i
                    if grid[r][c] != ' ' and grid[r][c] != char:
                        can_place = False
                        break
                
                if can_place:
                    # Place the word
                    for i, char in enumerate(word):
                        r = start_row + dr * i
                        c = start_col + dc * i
                        grid[r][c] = char
                    
                    # Record placement
                    if dr == 0 and dc == 1:
                        direction_name = "right"
                    elif dr == 1 and dc == 0:
                        direction_name = "down"
                    else:
                        direction_name = "diagonal"
                    
                    placements.append((word, start_row, start_col, direction_name))
                    placed = True
    
    # Fill remaining spaces with random letters
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == ' ':
                grid[r][c] = chr(ord('A') + random.randint(0, 25))
    
    # Output grid
    for row in grid:
        print(''.join(row))
    
    # Output word locations
    for word, row, col, direction in placements:
        print(f"{word}: row {row} col {col} {direction}")

if __name__ == "__main__":
    main()