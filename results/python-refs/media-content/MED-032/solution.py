import csv
import sys

# Read CSV from stdin
reader = csv.reader(sys.stdin)
rows = list(reader)

if not rows:
    sys.exit()

# Calculate column widths
col_widths = []
for col_idx in range(len(rows[0])):
    max_width = max(len(str(row[col_idx])) for row in rows)
    col_widths.append(max_width)

# Create separator row
separator = '+' + '+'.join('-' * (width + 2) for width in col_widths) + '+'

# Print table
print(separator)
for i, row in enumerate(rows):
    line = '|'
    for j, cell in enumerate(row):
        line += f' {str(cell).ljust(col_widths[j])} |'
    print(line)
    if i == 0:  # After header
        print(separator)

print(separator)