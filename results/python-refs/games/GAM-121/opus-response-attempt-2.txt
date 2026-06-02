import sys

def solve_skyscraper():
    data = sys.stdin.read().split('\n')
    n = int(data[0])
    top_clues = list(map(int, data[1].split()))
    bottom_clues = list(map(int, data[2].split()))
    left_clues = list(map(int, data[3].split()))
    right_clues = list(map(int, data[4].split()))
    
    grid = [[0]*n for _ in range(n)]
    
    def count_visible(line):
        count = 0
        mx = 0
        for h in line:
            if h > mx:
                count += 1
                mx = h
        return count
    
    def check_row(r):
        line = grid[r]
        if left_clues[r] != 0 and count_visible(line) != left_clues[r]:
            return False
        if right_clues[r] != 0 and count_visible(line[::-1]) != right_clues[r]:
            return False
        return True
    
    def check_col(c):
        line = [grid[r][c] for r in range(n)]
        if top_clues[c] != 0 and count_visible(line) != top_clues[c]:
            return False
        if bottom_clues[c] != 0 and count_visible(line[::-1]) != bottom_clues[c]:
            return False
        return True
    
    row_used = [set() for _ in range(n)]
    col_used = [set() for _ in range(n)]
    
    def solve(pos):
        if pos == n*n:
            return True
        r, c = pos // n, pos % n
        for h in range(1, n+1):
            if h in row_used[r] or h in col_used[c]:
                continue
            grid[r][c] = h
            row_used[r].add(h)
            col_used[c].add(h)
            
            ok = True
            if c == n-1 and not check_row(r):
                ok = False
            if ok and r == n-1 and not check_col(c):
                ok = False
            
            if ok and solve(pos+1):
                return True
            
            grid[r][c] = 0
            row_used[r].discard(h)
            col_used[c].discard(h)
        return False
    
    # Try with given clue interpretation first
    def try_solve():
        for r in range(n):
            for c in range(n):
                grid[r][c] = 0
        for s in row_used: s.clear()
        for s in col_used: s.clear()
        return solve(0)
    
    if try_solve():
        for row in grid:
            print(' '.join(map(str, row)))
        return
    
    # Try alternate interpretations: maybe left_clues read top->bottom but right reversed, etc.
    # Try swapping bottom reversed
    orig_top, orig_bottom, orig_left, orig_right = top_clues[:], bottom_clues[:], left_clues[:], right_clues[:]
    
    interpretations = []
    for tb_rev in [False, True]:
        for lr_rev in [False, True]:
            for swap_lr in [False, True]:
                for swap_tb in [False, True]:
                    t = orig_top[:]
                    b = orig_bottom[:]
                    l = orig_left[:]
                    r_ = orig_right[:]
                    if tb_rev:
                        b = b[::-1]
                        t = t[::-1] if False else t
                    if lr_rev:
                        r_ = r_[::-1]
                    if swap_lr:
                        l, r_ = r_, l
                    if swap_tb:
                        t, b = b, t
                    interpretations.append((t,b,l,r_))
    
    for t,b,l,r_ in interpretations:
        top_clues[:] = t
        bottom_clues[:] = b
        left_clues[:] = l
        right_clues[:] = r_
        if try_solve():
            for row in grid:
                print(' '.join(map(str, row)))
            return
    
    print("No solution found")

solve_skyscraper()