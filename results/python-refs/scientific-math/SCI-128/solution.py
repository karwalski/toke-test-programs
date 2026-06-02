import sys

def gaussian_elimination_partial_pivot(matrix):
    n = len(matrix)
    
    # Forward elimination with partial pivoting
    for i in range(n):
        # Find the row with maximum absolute value in column i
        max_row = i
        for k in range(i + 1, n):
            if abs(matrix[k][i]) > abs(matrix[max_row][i]):
                max_row = k
        
        # Check if pivot is zero (no unique solution)
        if abs(matrix[max_row][i]) < 1e-10:
            return None
        
        # Swap rows
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Make all rows below this one 0 in current column
        for k in range(i + 1, n):
            factor = matrix[k][i] / matrix[i][i]
            for j in range(i, n + 1):
                matrix[k][j] -= factor * matrix[i][j]
    
    # Back substitution
    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = matrix[i][n]
        for j in range(i + 1, n):
            solution[i] -= matrix[i][j] * solution[j]
        solution[i] /= matrix[i][i]
    
    return solution

# Read input
n = int(input())
matrix = []
for i in range(n):
    row = list(map(float, input().split()))
    matrix.append(row)

# Solve the system
solution = gaussian_elimination_partial_pivot(matrix)

if solution is None:
    print("NO UNIQUE SOLUTION")
else:
    output = []
    for i in range(len(solution)):
        output.append(f"x{i+1}={solution[i]:.6f}")
    print(" ".join(output))