def matrix_multiply(A, B, mod=None):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
                if mod:
                    C[i][j] %= mod
    return C

def matrix_power(matrix, b, mod=None):
    n = len(matrix)
    # Identity matrix
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    
    base = [row[:] for row in matrix]  # Copy matrix
    
    while b > 0:
        if b & 1:
            result = matrix_multiply(result, base, mod)
        base = matrix_multiply(base, base, mod)
        b >>= 1
    
    return result

def fast_power(a, b, mod=None):
    result = 1
    base = a
    while b > 0:
        if b & 1:
            result *= base
            if mod:
                result %= mod
        base *= base
        if mod:
            base %= mod
        b >>= 1
    return result

# Read input
type_input = input().strip()

if type_input == "int":
    a, b = map(int, input().split())
    result = fast_power(a, b)
    print(f"Result: {result}")
elif type_input == "modint":
    a, b, m = map(int, input().split())
    result = fast_power(a, b, m)
    print(f"Result: {result}")
elif type_input == "matrix":
    n = int(input())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    b = int(input())
    
    result_matrix = matrix_power(matrix, b)
    print("Result:")
    for row in result_matrix:
        print(" ".join(map(str, row)))