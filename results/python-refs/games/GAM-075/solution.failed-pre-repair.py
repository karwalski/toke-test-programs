import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Find the blank line separating grid and word list
    blank_idx = -1
    for i, line in enumerate(lines):
        if line == '':
            blank_idx = i
            break
    
    if blank_idx == -1:
        # No blank line found, assume all lines are grid
        grid = lines
        words = []
    else:
        grid = lines[:blank_idx]
        words = lines[blank_idx + 1:]
    
    return grid, words

def find_slots(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    slots = []
    
    # Find horizontal slots
    for r in range(rows):
        start = None
        for c in range(cols):
            if grid[r][c] != '#':
                if start is None:
                    start = c
            else:
                if start is not None and c - start >= 2:
                    slots.append(('H', r, start, c - 1))
                start = None
        if start is not None and cols - start >= 2:
            slots.append(('H', r, start, cols - 1))
    
    # Find vertical slots
    for c in range(cols):
        start = None
        for r in range(rows):
            if grid[r][c] != '#':
                if start is None:
                    start = r
            else:
                if start is not None and r - start >= 2:
                    slots.append(('V', start, c, r - 1))
                start = None
        if start is not None and rows - start >= 2:
            slots.append(('V', start, c, rows - 1))
    
    return slots

def get_slot_positions(slot):
    direction, *coords = slot
    positions = []
    
    if direction == 'H':
        r, start_c, end_c = coords
        for c in range(start_c, end_c + 1):
            positions.append((r, c))
    else:  # 'V'
        start_r, c, end_r = coords
        for r in range(start_r, end_r + 1):
            positions.append((r, c))
    
    return positions

def can_place_word(grid, slot, word):
    positions = get_slot_positions(slot)
    
    if len(word) != len(positions):
        return False
    
    for i, (r, c) in enumerate(positions):
        if grid[r][c] != '?' and grid[r][c] != word[i]:
            return False
    
    return True

def place_word(grid, slot, word):
    positions = get_slot_positions(slot)
    new_grid = [list(row) for row in grid]
    
    for i, (r, c) in enumerate(positions):
        new_grid[r][c] = word[i]
    
    return [''.join(row) for row in new_grid]

def solve(grid, slots, words, used_words, slot_idx):
    if slot_idx == len(slots):
        return grid
    
    slot = slots[slot_idx]
    
    for word in words:
        if word in used_words:
            continue
        
        if can_place_word(grid, slot, word):
            new_grid = place_word(grid, slot, word)
            new_used = used_words | {word}
            
            result = solve(new_grid, slots, words, new_used, slot_idx + 1)
            if result is not None:
                return result
    
    return None

def main():
    grid, words = read_input()
    
    if not grid or not words:
        print("No solution")
        return
    
    slots = find_slots(grid)
    
    result = solve(grid, slots, words, set(), 0)
    
    if result is None:
        print("No solution")
    else:
        for row in result:
            print(row)

if __name__ == "__main__":
    main()