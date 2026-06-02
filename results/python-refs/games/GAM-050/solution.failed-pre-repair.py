import sys

def main():
    # Read grid size
    grid_size = int(input().strip())
    
    # Read card layout
    cards_line = input().strip()
    cards = list(map(int, cards_line.split()))
    
    # Create grid
    grid = []
    for i in range(grid_size):
        row = cards[i * grid_size:(i + 1) * grid_size]
        grid.append(row)
    
    # Track matched cards
    matched = [[False] * grid_size for _ in range(grid_size)]
    score = 0
    
    # Process flip pairs
    try:
        while True:
            line = input().strip()
            if not line:
                break
            
            flip_pair = list(map(int, line.split()))
            pos1, pos2 = flip_pair[0], flip_pair[1]
            
            # Convert positions to row, col
            row1, col1 = pos1 // grid_size, pos1 % grid_size
            row2, col2 = pos2 // grid_size, pos2 % grid_size
            
            # Check if cards match and aren't already matched
            if (not matched[row1][col1] and not matched[row2][col2] and 
                grid[row1][col1] == grid[row2][col2] and 
                (row1, col1) != (row2, col2)):
                # Match found
                matched[row1][col1] = True
                matched[row2][col2] = True
                score += 1
                
    except EOFError:
        pass
    
    # Count remaining unmatched cards
    remaining = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if not matched[i][j]:
                remaining += 1
    
    print(f"Score: {score}")
    print(f"Remaining: {remaining}")

if __name__ == "__main__":
    main()