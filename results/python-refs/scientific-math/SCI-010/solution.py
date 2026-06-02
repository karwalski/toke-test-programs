def gauss_jordan_inverse(matrix):
    n = len(matrix)
    
    # Create augmented matrix [A|I]
    augmented = []
    for i in range(n):
        row = matrix[i][:] + [0] * n
        row[n + i] = 1
        augmented.append(row)
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = i
        for k in range(i + 1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Check for singular matrix
        if abs(augmented[i][i]) < 1e-10:
            return None
        
        # Make diagonal element 1
        pivot = augmented[i][i]
        for j in range(2 * n):
            augmented[i][j] /= pivot
        
        # Eliminate column
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(2 * n):
                    augmented[k][j] -= factor * augmented[i][j]
    
    # Extract inverse matrix
    inverse = []
    for i in range(n):
        inverse.append(augmented[i][n:])
    
    return inverse

# Read input
n = int(input())
matrix = []
for _ in range(n):
    row = list(map(float, input().split()))
    matrix.append(row)

# Compute inverse
inverse = gauss_jordan_inverse(matrix)

# Output result
if inverse is None:
    print("ERROR")
else:
    for row in inverse:
        print(" ".join(f"{x:.6f}" for x in row))