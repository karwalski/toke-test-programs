import sys

# Read the board from stdin
board = []
for _ in range(10):
    line = input().strip()
    board.append(list(line))

# Find completed lines (lines with all X's)
lines_to_remove = []
for i in range(10):
    if all(cell == 'X' for cell in board[i]):
        lines_to_remove.append(i)

# Count of lines cleared
lines_cleared = len(lines_to_remove)

# Remove completed lines from bottom to top to avoid index issues
for i in reversed(lines_to_remove):
    board.pop(i)

# Add empty lines at the top
for _ in range(lines_cleared):
    board.insert(0, ['.'] * 10)

# Output the result
print(lines_cleared)
for row in board:
    print(''.join(row))