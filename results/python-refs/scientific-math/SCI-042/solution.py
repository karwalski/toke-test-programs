import sys

def fibonacci_recursive_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibonacci_recursive_memo(n-1, memo) + fibonacci_recursive_memo(n-2, memo)
    return memo[n]

def fibonacci_iterative(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

def matrix_multiply(A, B):
    return [[A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]]

def matrix_power(matrix, n):
    if n == 1:
        return matrix
    if n % 2 == 0:
        half = matrix_power(matrix, n // 2)
        return matrix_multiply(half, half)
    else:
        return matrix_multiply(matrix, matrix_power(matrix, n - 1))

def fibonacci_matrix(n):
    if n <= 1:
        return n
    base_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power(base_matrix, n)
    return result_matrix[0][1]

# Read input
n = int(input().strip())
method = input().strip()

# Compute Fibonacci sequence
fib_sequence = []
for i in range(n + 1):
    if method == "recursive":
        fib_sequence.append(fibonacci_recursive_memo(i))
    elif method == "iterative":
        fib_sequence.append(fibonacci_iterative(i))
    elif method == "matrix":
        fib_sequence.append(fibonacci_matrix(i))

# Output
print(" ".join(map(str, fib_sequence)))