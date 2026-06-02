import sys

# Read all input lines
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:
        lines.append(line.split())

# Calculate transpose
if lines:
    rows = len(lines)
    cols = len(lines[0])
    
    # Print transposed matrix
    for j in range(cols):
        row = []
        for i in range(rows):
            row.append(lines[i][j])
        print(' '.join(row))