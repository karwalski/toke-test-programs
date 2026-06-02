import math

def qr_decomposition_gram_schmidt(A):
    m, n = len(A), len(A[0])
    
    # Initialize Q and R matrices
    Q = [[0.0 for _ in range(n)] for _ in range(m)]
    R = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # Extract columns from A
    columns = []
    for j in range(n):
        col = [A[i][j] for i in range(m)]
        columns.append(col)
    
    # Classical Gram-Schmidt orthogonalization
    for j in range(n):
        # Start with the j-th column of A
        v = columns[j][:]
        
        # Subtract projections onto previous orthonormal vectors
        for i in range(j):
            # Compute projection coefficient r_ij = q_i^T * a_j
            r_ij = sum(Q[k][i] * columns[j][k] for k in range(m))
            R[i][j] = r_ij
            
            # Subtract projection: v = v - r_ij * q_i
            for k in range(m):
                v[k] -= r_ij * Q[k][i]
        
        # Compute norm of v
        norm_v = math.sqrt(sum(x*x for x in v))
        R[j][j] = norm_v
        
        # Normalize v to get q_j
        for k in range(m):
            Q[k][j] = v[k] / norm_v
    
    return Q, R

# Read input
m, n = map(int, input().split())
A = []
for _ in range(m):
    row = list(map(float, input().split()))
    A.append(row)

# Compute QR decomposition
Q, R = qr_decomposition_gram_schmidt(A)

# Output Q matrix
for i in range(m):
    row_str = " ".join(f"{Q[i][j]:.6f}" for j in range(n))
    print(row_str)

# Blank line
print()

# Output R matrix
for i in range(n):
    row_str = " ".join(f"{R[i][j]:.6f}" for j in range(n))
    print(row_str)