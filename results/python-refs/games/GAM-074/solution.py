import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Parse snakes and ladders
    snakes = {}
    ladders = {}
    i = 0
    
    # Read snakes and ladders until blank line
    while i < len(lines) and lines[i].strip():
        line = lines[i].strip()
        from_pos, to_pos = map(int, line.split(':'))
        if from_pos > to_pos:
            snakes[from_pos] = to_pos
        else:
            ladders[from_pos] = to_pos
        i += 1
    
    # Skip blank line
    i += 1
    
    # Read dice rolls
    dice_rolls = list(map(int, lines[i].split()))
    
    # Simulate game
    position = 0
    
    for roll in dice_rolls:
        position += roll
        
        # Check for ladders
        if position in ladders:
            position = ladders[position]
        # Check for snakes
        elif position in snakes:
            position = snakes[position]
        
        print(position)

if __name__ == "__main__":
    main()