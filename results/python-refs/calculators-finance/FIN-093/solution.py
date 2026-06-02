import sys
import math

def power_method(matrix, max_iterations, tolerance):
    n = len(matrix)
    x = [1.0] * n
    norm = math.sqrt(sum(val**2 for val in x))
    x = [val / norm for val in x]
    
    eigenvalue = 0
    
    for iteration in range(max_iterations):
        y = [0.0] * n
        for i in range(n):
            for j in range(n):
                y[i] += matrix[i][j] * x[j]
        
        # Rayleigh quotient: x^T A x / x^T x (x is normalized)
        new_eigenvalue = sum(x[i] * y[i] for i in range(n))
        
        norm = math.sqrt(sum(val**2 for val in y))
        x_new = [val / norm for val in y]
        
        if iteration > 0:
            if abs(new_eigenvalue - eigenvalue) < tolerance:
                eigenvalue = new_eigenvalue
                x = x_new
                break
        
        eigenvalue = new_eigenvalue
        x = x_new
    
    # Ensure positive first component
    if x[0] < 0:
        x = [-v for v in x]
    
    return eigenvalue, x

lines = []
for line in sys.stdin:
    if line.strip():
        lines.append(line.strip())

matrix_lines = lines[:-1]
params = lines[-1].split()
max_iterations = int(params[0])
tolerance = float(params[1])

matrix = []
for line in matrix_lines:
    row = [float(x) for x in line.split()]
    matrix.append(row)

eigenvalue, eigenvector = power_method(matrix, max_iterations, tolerance)

print(f"{eigenvalue:.4f}")
print(" ".join(f"{val:.4f}" for val in eigenvector))