import sys

# Read input
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:
        lines.append(line)

# Parse the grid
grid = []
for line in lines:
    row = list(map(int, line.split()))
    grid.append(row)

n = len(grid)

# Calculate the expected sum (sum of first row)
expected_sum = sum(grid[0])

# Check if it's a magic square
is_magic = True

# Check all rows
for i in range(n):
    if sum(grid[i]) != expected_sum:
        is_magic = False
        break

# Check all columns
if is_magic:
    for j in range(n):
        col_sum = sum(grid[i][j] for i in range(n))
        if col_sum != expected_sum:
            is_magic = False
            break

# Check main diagonal (top-left to bottom-right)
if is_magic:
    diag_sum = sum(grid[i][i] for i in range(n))
    if diag_sum != expected_sum:
        is_magic = False

# Check anti-diagonal (top-right to bottom-left)
if is_magic:
    anti_diag_sum = sum(grid[i][n-1-i] for i in range(n))
    if anti_diag_sum != expected_sum:
        is_magic = False

# Output result
if is_magic:
    print(f"Magic square with sum {expected_sum}")
else:
    print("Not a magic square")