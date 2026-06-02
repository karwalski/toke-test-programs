# Read dimensions of matrix A
m, k = map(int, input().split())

# Read matrix A
A = []
for i in range(m):
    row = list(map(float, input().split()))
    A.append(row)

# Read dimensions for matrix B
k2, n = map(int, input().split())

# Read matrix B
B = []
for i in range(k2):
    row = list(map(float, input().split()))
    B.append(row)

# Multiply matrices A and B
C = []
for i in range(m):
    row = []
    for j in range(n):
        sum_val = 0
        for l in range(k):
            sum_val += A[i][l] * B[l][j]
        row.append(sum_val)
    C.append(row)

# Output the result matrix
for i in range(m):
    output_row = []
    for j in range(n):
        output_row.append(f"{C[i][j]:.4f}")
    print(" ".join(output_row))