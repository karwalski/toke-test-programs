import sys

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line that separates ships from shots
    blank_line_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_line_idx = i
            break
    
    # Parse ships
    ships = {}
    for i in range(blank_line_idx):
        parts = lines[i].split()
        name = parts[0]
        start_row = int(parts[1])
        start_col = int(parts[2])
        end_row = int(parts[3])
        end_col = int(parts[4])
        
        # Generate all coordinates for this ship
        coords = set()
        if start_row == end_row:  # horizontal ship
            for col in range(min(start_col, end_col), max(start_col, end_col) + 1):
                coords.add((start_row, col))
        else:  # vertical ship
            for row in range(min(start_row, end_row), max(start_row, end_row) + 1):
                coords.add((row, start_col))
        
        ships[name] = coords
    
    # Process shots
    ship_hits = {name: set() for name in ships}
    
    for i in range(blank_line_idx + 1, len(lines)):
        if lines[i] == '':
            continue
        parts = lines[i].split()
        shot_row = int(parts[0])
        shot_col = int(parts[1])
        shot_coord = (shot_row, shot_col)
        
        hit = False
        for ship_name, ship_coords in ships.items():
            if shot_coord in ship_coords:
                hit = True
                ship_hits[ship_name].add(shot_coord)
                
                # Check if ship is sunk
                if ship_hits[ship_name] == ship_coords:
                    print(f"Sunk {ship_name}")
                else:
                    print("Hit")
                break
        
        if not hit:
            print("Miss")

if __name__ == "__main__":
    main()