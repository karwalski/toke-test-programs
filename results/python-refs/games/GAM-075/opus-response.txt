import sys

def read_input():
    data = sys.stdin.read().split('\n')
    # remove trailing empty if any from final newline, but keep blank separator
    while data and data[-1] == '':
        data.pop()
    
    blank_idx = -1
    for i, line in enumerate(data):
        if line == '':
            blank_idx = i
            break
    
    if blank_idx == -1:
        grid = data
        words = []
    else:
        grid = data[:blank_idx]
        words = [w for w in data[blank_idx + 1:] if w != '']
    
    return grid, words

def find_slots(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    slots = []
    
    # Horizontal slots (length >= 1, but only if multi-cell or part of intersection)
    # Actually accept length >= 1
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
    direction = slot[0]
    if direction == 'H':
        r, start_c, end_c = slot[1], slot[2], slot[3]
        return [(r, c) for c in range(start_c, end_c + 1)]
    else:
        start_r, c, end_r = slot[1], slot[2], slot[3]
        return [(r, c) for r in range(start_r, end_r + 1)]

def can_place_word(grid, slot, word):
    positions = get_slot_positions(slot)
    if len(word) != len(positions):
        return False
    for i, (r, c) in enumerate(positions):
        ch = grid[r][c]
        if ch != '?' and ch != word[i]:
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

def grid_complete(grid):
    for row in grid:
        if '?' in row:
            return False
    return True

def solve_cells(grid, words, used):
    # Find first '?'
    rows = len(grid)
    cols = len(grid[0])
    target = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '?':
                target = (r, c)
                break
        if target:
            break
    if target is None:
        # Check all slots filled with valid words
        slots = find_slots(grid)
        for s in slots:
            positions = get_slot_positions(s)
            w = ''.join(grid[r][c] for r,c in positions)
            if w not in words:
                return None
        return grid
    
    # Try all letters that could go here based on words
    # Actually easier: try placing each unused word in some slot containing this cell
    slots = find_slots(grid)
    containing = []
    for s in slots:
        if target in get_slot_positions(s):
            containing.append(s)
    
    if not containing:
        # isolated cell, try any letter from words
        tried = set()
        for w in words:
            for ch in w:
                if ch in tried:
                    continue
                tried.add(ch)
                new_grid = [list(row) for row in grid]
                new_grid[target[0]][target[1]] = ch
                new_grid = [''.join(row) for row in new_grid]
                result = solve_cells(new_grid, words, used)
                if result:
                    return result
        return None
    
    slot = containing[0]
    for word in words:
        if word in used:
            continue
        if can_place_word(grid, slot, word):
            new_grid = place_word(grid, slot, word)
            result = solve_cells(new_grid, words, used | {word})
            if result is not None:
                return result
    return None

def main():
    grid, words = read_input()
    
    if not grid:
        print("No solution")
        return
    
    slots = find_slots(grid)
    
    if slots:
        result = solve(grid, slots, words, set(), 0)
        if result is not None and grid_complete(result):
            for row in result:
                print(row)
            return
    
    # Fallback: cell-by-cell with words constraint
    result = solve_cells(grid, words, set())
    if result is None:
        print("No solution")
    else:
        for row in result:
            print(row)

if __name__ == "__main__":
    main()