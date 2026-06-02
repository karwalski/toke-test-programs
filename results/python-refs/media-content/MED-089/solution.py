import sys

# Read input
lines = sys.stdin.read().strip().split('\n')
n = int(lines[0])
items = lines[1:]

if not items:
    sys.exit()

# Calculate number of rows needed
num_items = len(items)
rows = (num_items + n - 1) // n  # Ceiling division

# Create grid
grid = []
for r in range(rows):
    row = []
    for c in range(n):
        idx = r * n + c
        if idx < num_items:
            row.append(items[idx])
        else:
            row.append("")
    grid.append(row)

# Calculate column widths (width of widest item in each column)
col_widths = [0] * n
for c in range(n):
    for r in range(rows):
        if grid[r][c]:
            col_widths[c] = max(col_widths[c], len(grid[r][c]))

# Print output
for r in range(rows):
    row_output = []
    for c in range(n):
        if grid[r][c]:
            if c == n - 1:  # Last column, no padding needed
                row_output.append(grid[r][c])
            else:
                row_output.append(grid[r][c].ljust(col_widths[c]))
    
    # Join with single space and remove trailing whitespace
    print(' '.join(row_output).rstrip())