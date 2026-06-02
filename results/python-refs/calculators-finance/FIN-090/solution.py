import sys

# Read all input
lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

# Find the blank line that separates the two matrices
blank_line_index = lines.index('')

# Parse matrix A
matrix_a = []
for i in range(blank_line_index):
    row = list(map(int, lines[i].split()))
    matrix_a.append(row)

# Parse matrix B
matrix_b = []
for i in range(blank_line_index + 1, len(lines)):
    row = list(map(int, lines[i].split()))
    matrix_b.append(row)

# Get dimensions
rows_a = len(matrix_a)
cols_a = len(matrix_a[0])
rows_b = len(matrix_b)
cols_b = len(matrix_b[0])

# Multiply matrices
result = []
for i in range(rows_a):
    row = []
    for j in range(cols_b):
        sum_val = 0
        for k in range(cols_a):
            sum_val += matrix_a[i][k] * matrix_b[k][j]
        row.append(sum_val)
    result.append(row)

# Output result
for row in result:
    print(' '.join(map(str, row)))