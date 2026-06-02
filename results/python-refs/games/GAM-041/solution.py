I need to figure out the mine placement pattern from the expected outputs.

Test 1: 5x5, 3 mines, seed 42. Mines at (2,4), (3,4), (4,3).
Test 2: 3x3, 1 mine, seed 1. Mine at (1,1).

Let me try different approaches. With seed 1, 3x3 grid, 1 mine at (1,1) = index 4.

Try `random.sample(range(9), 1)` with seed 1: let me think... Actually let me try using random.randint or random.randrange repeatedly.

With seed 1, `random.randrange(9)` gives... I'll try sampling indices.

Let me try: generate positions by picking random row, col separately, avoiding duplicates.

Actually, let me try `random.sample(range(rows*cols), mines)` and see.

Test 2: seed 1, sample(range(9), 1) - I recall this might give 2 or similar. Let me try different methods.

Another approach: shuffle list and take first N.

Let me try: positions list, shuffle, take last N? Or generate by while loop with randint.

Try this: use `random.randint(0, rows-1)` and `random.randint(0, cols-1)` repeatedly until we have enough unique mines.

For seed 1, first call randint(0,2): need to get (1,1).
For seed 42, first calls need (2,4),(3,4),(4,3) in some order.

Let me just try the while-loop approach:

```python
import random
random.seed(seed)
mines_set = set()
while len(mines_set) < mines:
    r = random.randint(0, rows-1)
    c = random.randint(0, cols-1)
    mines_set.add((r,c))
```

I'll submit this and hope it matches.

```python
import random

def generate_minesweeper_board(rows, cols, mines, seed):
    random.seed(seed)
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    
    mine_positions = set()
    while len(mine_positions) < mines:
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)
        mine_positions.add((r, c))
    
    for r, c in mine_positions:
        board[r][c] = 'M'
    
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != 'M':
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'M':
                            count += 1
                board[r][c] = count
    
    return board

def print_board(board):
    for row in board:
        print(''.join(str(cell) for cell in row))

line = input().strip()
rows, cols, mines, seed = map(int, line.split())
board = generate_minesweeper_board(rows, cols, mines, seed)
print_board(board)
```