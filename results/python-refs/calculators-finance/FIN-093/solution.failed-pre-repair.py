import sys
import math

def power_method(matrix, max_iterations, tolerance):
    n = len(matrix)
    
    # Initialize eigenvector guess (start with all ones)
    x = [1.0] * n
    
    # Normalize initial vector
    norm = math.sqrt(sum(val**2 for val in x))
    x = [val / norm for val in x]
    
    eigenvalue = 0
    
    for iteration in range(max_iterations):
        # Matrix-vector multiplication: y = A * x
        y = [0.0] * n
        for i in range(n):
            for j in range(n):
                y[i] += matrix[i][j] * x[j]
        
        # Find the dominant eigenvalue (component with largest absolute value)
        new_eigenvalue = max(y, key=abs)
        
        # Normalize the vector
        norm = math.sqrt(sum(val**2 for val in y))
        x_new = [val / norm for val in y]
        
        # Check for convergence
        if iteration > 0:
            if abs(new_eigenvalue - eigenvalue) < tolerance:
                break
        
        eigenvalue = new_eigenvalue
        x = x_new
    
    return eigenvalue, x

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse matrix
matrix_lines = lines[:-1]
params = lines[-1].split()
max_iterations = int(params[0])
tolerance = float(params[1])

# Build matrix
matrix = []
for line in matrix_lines:
    row = [float(x) for x in line.split()]
    matrix.append(row)

# Solve using power method
eigenvalue, eigenvector = power_method(matrix, max_iterations, tolerance)

# Output results
print(f"{eigenvalue:.4f}")
print(" ".join(f"{val:.4f}" for val in eigenvector))