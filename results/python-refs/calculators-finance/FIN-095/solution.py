import sys

def gaussian_elimination(matrix):
    n = len(matrix)
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            if matrix[i][i] != 0:
                factor = matrix[k][i] / matrix[i][i]
                for j in range(i, n + 1):
                    matrix[k][j] -= factor * matrix[i][j]
    
    # Back substitution
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n]
        for j in range(i + 1, n):
            solution[i] -= matrix[i][j] * solution[j]
        solution[i] /= matrix[i][i]
    
    return solution

# Read input
lines = []
for line in sys.stdin:
    line = line.strip()
    if line:
        lines.append(line)

# Parse augmented matrix
matrix = []
for line in lines:
    row = list(map(float, line.split()))
    matrix.append(row)

# Solve system
solution = gaussian_elimination(matrix)

# Output results
for i, val in enumerate(solution):
    print(f"x{i+1}={val:.4f}")