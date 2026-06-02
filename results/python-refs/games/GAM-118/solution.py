import sys

def solve():
    data = sys.stdin.read().split('\n')
    rows = [line for line in data if line.strip()]
    grid = [list(map(int, r.split())) for r in rows]
    n = len(grid)
    total = n * n
    # Find position of each anchor number
    pos_of = {}
    for i in range(n):
        for j in range(n):
            v = grid[i][j]
            if v != 0:
                pos_of[v] = (i, j)
    # Find starting position (number 1) or any anchor to start backtracking
    # We will place numbers 1..total in order
    # If 1 is not given, try every cell as start
    def neighbors(r, c):
        for dr, dc in ((-1,0),(1,0),(0,-1),(0,1)):
            nr, nc = r+dr, c+dc
            if 0 <= nr < n and 0 <= nc < n:
                yield nr, nc
    
    sol = [row[:] for row in grid]
    
    def backtrack(num, r, c):
        # num is currently placed at (r,c); place num+1 next
        if num == total:
            return True
        nxt = num + 1
        if nxt in pos_of:
            tr, tc = pos_of[nxt]
            # must be adjacent
            if abs(tr-r)+abs(tc-c) == 1 and sol[tr][tc] == nxt:
                if backtrack(nxt, tr, tc):
                    return True
            return False
        else:
            for nr, nc in neighbors(r, c):
                if sol[nr][nc] == 0:
                    sol[nr][nc] = nxt
                    if backtrack(nxt, nr, nc):
                        return True
                    sol[nr][nc] = 0
            return False
    
    if 1 in pos_of:
        r, c = pos_of[1]
        backtrack(1, r, c)
    else:
        # try each empty cell as start
        found = False
        for i in range(n):
            if found: break
            for j in range(n):
                if sol[i][j] == 0:
                    sol[i][j] = 1
                    if backtrack(1, i, j):
                        found = True
                        break
                    sol[i][j] = 0
        # also handle case where 1 not anchor but some other is
    
    out = []
    width = len(str(total))
    for row in sol:
        out.append(' '.join(str(x).rjust(width) for x in row))
    print('\n'.join(out))

solve()
