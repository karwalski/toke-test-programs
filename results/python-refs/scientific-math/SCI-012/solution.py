import sys

def lu_decomposition_partial_pivoting(A):
    n = len(A)
    # Create copies to avoid modifying original
    U = [row[:] for row in A]
    L = [[0.0] * n for _ in range(n)]
    P = list(range(n))
    
    # Initialize L as identity matrix
    for i in range(n):
        L[i][i] = 1.0
    
    for k in range(n):
        # Find pivot (row with maximum absolute value in column k)
        max_val = abs(U[k][k])
        pivot_row = k
        for i in range(k + 1, n):
            if abs(U[i][k]) > max_val:
                max_val = abs(U[i][k])
                pivot_row = i
        
        # Swap rows in U, L (below diagonal), and P
        if pivot_row != k:
            U[k], U[pivot_row] = U[pivot_row], U[k]
            P[k], P[pivot_row] = P[pivot_row], P[k]
            # Swap the parts of L that have been computed (below diagonal)
            for j in range(k):
                L[k][j], L[pivot_row][j] = L[pivot_row][j], L[k][j]
        
        # Elimination
        for i in range(k + 1, n):
            if U[k][k] != 0:
                factor = U[i][k] / U[k][k]
                L[i][k] = factor
                for j in range(k, n):
                    U[i][j] -= factor * U[k][j]
    
    return L, U, P

def main():
    n = int(input().strip())
    A = []
    for _ in range(n):
        row = list(map(float, input().strip().split()))
        A.append(row)
    
    L, U, P = lu_decomposition_partial_pivoting(A)
    
    # Output L matrix
    for i in range(n):
        row_str = " ".join(f"{L[i][j]:.6f}" for j in range(n))
        print(row_str)
    
    print()  # Blank line
    
    # Output U matrix
    for i in range(n):
        row_str = " ".join(f"{U[i][j]:.6f}" for j in range(n))
        print(row_str)
    
    print()  # Blank line
    
    # Output P (permutation indices)
    p_str = " ".join(str(P[i]) for i in range(n))
    print(p_str)

if __name__ == "__main__":
    main()