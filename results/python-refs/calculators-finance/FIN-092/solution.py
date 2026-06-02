import sys

def determinant_2x2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

def inverse_2x2(matrix):
    det = determinant_2x2(matrix)
    if det == 0:
        return None
    
    inv_det = 1.0 / det
    inverse = [
        [matrix[1][1] * inv_det, -matrix[0][1] * inv_det],
        [-matrix[1][0] * inv_det, matrix[0][0] * inv_det]
    ]
    return inverse

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse matrix
matrix = []
for line in lines:
    row = list(map(float, line.split()))
    matrix.append(row)

# Calculate inverse
inverse = inverse_2x2(matrix)

# Output result
for row in inverse:
    formatted_row = [f"{val:.4f}" for val in row]
    print(" ".join(formatted_row))