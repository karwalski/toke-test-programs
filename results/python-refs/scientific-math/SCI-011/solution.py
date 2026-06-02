def lu_decomposition(matrix):
    n = len(matrix)
    
    # Create copies for L and U matrices
    L = [[0.0 for _ in range(n)] for _ in range(n)]
    U = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # Initialize L as identity matrix
    for i in range(n):
        L[i][i] = 1.0
    
    # Perform LU decomposition
    for i in range(n):
        # Upper triangular matrix U
        for k in range(i, n):
            sum_val = 0.0
            for j in range(i):
                sum_val += L[i][j] * U[j][k]
            U[i][k] = matrix[i][k] - sum_val
        
        # Lower triangular matrix L
        for k in range(i + 1, n):
            sum_val = 0.0
            for j in range(i):
                sum_val += L[k][j] * U[j][i]
            L[k][i] = (matrix[k][i] - sum_val) / U[i][i]
    
    return L, U

def determinant_from_lu(L, U):
    n = len(L)
    det_L = 1.0
    det_U = 1.0
    
    # Determinant of L (diagonal elements)
    for i in range(n):
        det_L *= L[i][i]
    
    # Determinant of U (diagonal elements)
    for i in range(n):
        det_U *= U[i][i]
    
    return det_L * det_U

# Read input
n = int(input())
matrix = []
for _ in range(n):
    row = list(map(float, input().split()))
    matrix.append(row)

# Compute LU decomposition and determinant
L, U = lu_decomposition(matrix)
det = determinant_from_lu(L, U)

# Output result
print(f"Determinant: {det:.6f}")