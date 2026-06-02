import sys
from collections import defaultdict

def solve_codeword():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    # Parse grid (lines of space-separated numbers)
    grid = []
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            continue
        # Check if this is a grid line (no '=' and tokens are numbers)
        if '=' in s:
            break
        tokens = s.split()
        try:
            row = [int(t) for t in tokens]
            grid.append(row)
            i += 1
        except ValueError:
            break
    
    # Parse known assignments line (may contain multiple "N=L" separated by space)
    known = {}
    while i < len(lines):
        s = lines[i].strip()
        if not s:
            i += 1
            break
        if '=' not in s:
            break
        tokens = s.split()
        all_assignments = True
        for tok in tokens:
            if '=' in tok:
                parts = tok.split('=')
                if len(parts) == 2:
                    try:
                        num = int(parts[0])
                        letter = parts[1].upper()
                        known[num] = letter
                    except ValueError:
                        all_assignments = False
                        break
                else:
                    all_assignments = False
                    break
            else:
                all_assignments = False
                break
        i += 1
        if not all_assignments:
            break
    
    # Skip blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1
    
    # Parse dictionary
    dictionary = []
    while i < len(lines):
        s = lines[i].strip()
        if s:
            dictionary.append(s.upper())
        i += 1
    
    if not grid:
        print("No solution")
        return
    
    rows = len(grid)
    cols = max(len(r) for r in grid)
    # Pad grid
    for r in grid:
        while len(r) < cols:
            r.append(0)
    
    # Find words (horizontal & vertical runs of length >= 2)
    words_positions = []
    
    for r in range(rows):
        c = 0
        while c < cols:
            if grid[r][c] != 0:
                start = c
                while c < cols and grid[r][c] != 0:
                    c += 1
                if c - start >= 2:
                    words_positions.append([(r, cc) for cc in range(start, c)])
            else:
                c += 1
    
    for c in range(cols):
        r = 0
        while r < rows:
            if grid[r][c] != 0:
                start = r
                while r < rows and grid[r][c] != 0:
                    r += 1
                if r - start >= 2:
                    words_positions.append([(rr, c) for rr in range(start, r)])
            else:
                r += 1
    
    words_by_length = defaultdict(list)
    for word in dictionary:
        words_by_length[len(word)].append(word)
    
    num_to_letter = dict(known)
    letter_to_num = {v: k for k, v in known.items()}
    
    def try_assign(positions, word):
        changes = []
        for pos, letter in zip(positions, word):
            num = grid[pos[0]][pos[1]]
            if num in num_to_letter:
                if num_to_letter[num] != letter:
                    # rollback
                    for n, l in changes:
                        del num_to_letter[n]
                        del letter_to_num[l]
                    return None
            else:
                if letter in letter_to_num:
                    for n, l in changes:
                        del num_to_letter[n]
                        del letter_to_num[l]
                    return None
                num_to_letter[num] = letter
                letter_to_num[letter] = num
                changes.append((num, letter))
        return changes
    
    def undo(changes):
        for n, l in changes:
            del num_to_letter[n]
            del letter_to_num[l]
    
    def backtrack(idx):
        if idx >= len(words_positions):
            return True
        positions = words_positions[idx]
        L = len(positions)
        for word in words_by_length.get(L, []):
            changes = try_assign(positions, word)
            if changes is not None:
                if backtrack(idx + 1):
                    return True
                undo(changes)
        return False
    
    if backtrack(0):
        out_lines = []
        for r in range(rows):
            parts = []
            for c in range(cols):
                num = grid[r][c]
                if num == 0:
                    continue
                if num in num_to_letter:
                    parts.append(f"{num}={num_to_letter[num]}")
                else:
                    parts.append(str(num))
            out_lines.append(' '.join(parts))
        print('\n'.join(out_lines))
    else:
        print("No solution")

solve_codeword()