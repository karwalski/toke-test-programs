import sys
import math

def normalize_vector(v):
    """Normalize a vector to unit length"""
    norm = math.sqrt(sum(x*x for x in v))
    return [x/norm for x in v]

def matrix_vector_multiply(matrix, vector):
    """Multiply matrix by vector"""
    n = len(matrix)
    result = []
    for i in range(n):
        sum_val = sum(matrix[i][j] * vector[j] for j in range(n))
        result.append(sum_val)
    return result

def dot_product(v1, v2):
    """Compute dot product of two vectors"""
    return sum(a*b for a, b in zip(v1, v2))

def rayleigh_quotient(matrix, vector):
    """Compute Rayleigh quotient: v^T * A * v / (v^T * v)"""
    av = matrix_vector_multiply(matrix, vector)
    return dot_product(vector, av) / dot_product(vector, vector)

# Read input
n = int(input().strip())
matrix = []
for i in range(n):
    row = list(map(float, input().strip().split()))
    matrix.append(row)

max_iterations = int(input().strip())
tolerance = float(input().strip())

# Initialize with vector of ones
x = [1.0] * n
x = normalize_vector(x)

prev_eigenvalue = 0.0

for iteration in range(max_iterations):
    # Multiply by matrix
    y = matrix_vector_multiply(matrix, x)
    
    # Compute eigenvalue estimate (Rayleigh quotient)
    eigenvalue = rayleigh_quotient(matrix, x)
    
    # Print iteration info
    print(f"Iteration {iteration + 1}: eigenvalue={eigenvalue:.6f}")
    
    # Normalize the result vector
    x = normalize_vector(y)
    
    # Check convergence
    if iteration > 0 and abs(eigenvalue - prev_eigenvalue) < tolerance:
        break
    
    prev_eigenvalue = eigenvalue

# Final eigenvalue and eigenvector
final_eigenvalue = rayleigh_quotient(matrix, x)
print(f"Dominant eigenvalue: {final_eigenvalue:.6f}")

# Format eigenvector output
eigenvector_str = " ".join(f"{v:.6f}" for v in x)
print(f"Eigenvector: {eigenvector_str}")