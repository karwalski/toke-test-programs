import sys

# Read input
lines = sys.stdin.read().strip().split('\n')

separator_in = lines[0]
separator_out = lines[1]
alignment = lines[2]
data_lines = lines[3:]

# Parse data into columns
rows = []
max_cols = 0
for line in data_lines:
    cols = line.split(separator_in)
    rows.append(cols)
    max_cols = max(max_cols, len(cols))

# Calculate column widths
col_widths = [0] * max_cols
for row in rows:
    for i, col in enumerate(row):
        col_widths[i] = max(col_widths[i], len(col))

# Format and output
for row in rows:
    formatted_cols = []
    for i in range(max_cols):
        if i < len(row):
            text = row[i]
        else:
            text = ""
        
        width = col_widths[i]
        
        if alignment == "left":
            formatted = text.ljust(width)
        elif alignment == "right":
            formatted = text.rjust(width)
        elif alignment == "center":
            formatted = text.center(width)
        
        formatted_cols.append(formatted)
    
    print(separator_out.join(formatted_cols).rstrip())