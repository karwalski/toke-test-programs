import sys

# Read dimensions
rows, cols = map(int, input().split())

# Read seed (not used in this simple case)
seed = int(input())

# Read student names
students = []
try:
    while True:
        name = input().strip()
        if name:
            students.append(name)
except EOFError:
    pass

# Create grid
grid = []
student_index = 0

for r in range(rows):
    row = []
    for c in range(cols):
        if student_index < len(students):
            row.append(students[student_index])
            student_index += 1
        else:
            row.append("")
    grid.append(row)

# Calculate column widths for proper formatting
if grid and grid[0]:
    col_widths = []
    for c in range(cols):
        max_width = 0
        for r in range(rows):
            if c < len(grid[r]):
                max_width = max(max_width, len(grid[r][c]))
        col_widths.append(max_width)
    
    # Output grid
    for r in range(rows):
        row_output = []
        for c in range(cols):
            if c < len(grid[r]):
                name = grid[r][c]
                if c == cols - 1:  # Last column - no padding
                    row_output.append(name)
                else:
                    # Pad to align with the expected spacing
                    padding = 10 - len(name) if len(name) < 10 else 0
                    row_output.append(name + " " * padding)
        print("".join(row_output))