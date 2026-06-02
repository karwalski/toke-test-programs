import sys

def determinant_2x2(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

def determinant_3x3(matrix):
    a = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
    b = matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
    c = matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    return a - b + c

def determinant_4x4(matrix):
    det = 0
    for col in range(4):
        # Create 3x3 submatrix by removing row 0 and column 'col'
        submatrix = []
        for i in range(1, 4):
            row = []
            for j in range(4):
                if j != col:
                    row.append(matrix[i][j])
            submatrix.append(row)
        
        cofactor = matrix[0][col] * determinant_3x3(submatrix)
        if col % 2 == 0:
            det += cofactor
        else:
            det -= cofactor
    return det

# Read input
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:
        lines.append(line)

# Parse matrix
matrix = []
for line in lines:
    row = [int(x) for x in line.split()]
    matrix.append(row)

n = len(matrix)

if n == 1:
    det = matrix[0][0]
elif n == 2:
    det = determinant_2x2(matrix)
elif n == 3:
    det = determinant_3x3(matrix)
elif n == 4:
    det = determinant_4x4(matrix)

print(det)