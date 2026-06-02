import sys

# Read input
x_line = input().strip()
y_line = input().strip()

# Parse x and y values
x_values = [float(x) for x in x_line.split(',')]
y_values = [float(y) for y in y_line.split(',')]

n = len(x_values)

# Set up the normal equations for least squares fitting
# We need to solve the system:
# [sum(x^4)  sum(x^3)  sum(x^2)] [a]   [sum(x^2*y)]
# [sum(x^3)  sum(x^2)  sum(x^1)] [b] = [sum(x*y)  ]
# [sum(x^2)  sum(x^1)  sum(1)  ] [c]   [sum(y)    ]

# Calculate sums
sum_x4 = sum(x**4 for x in x_values)
sum_x3 = sum(x**3 for x in x_values)
sum_x2 = sum(x**2 for x in x_values)
sum_x1 = sum(x for x in x_values)
sum_1 = n

sum_x2y = sum(x**2 * y for x, y in zip(x_values, y_values))
sum_xy = sum(x * y for x, y in zip(x_values, y_values))
sum_y = sum(y_values)

# Coefficient matrix
A = [
    [sum_x4, sum_x3, sum_x2],
    [sum_x3, sum_x2, sum_x1],
    [sum_x2, sum_x1, sum_1]
]

# Right-hand side vector
b = [sum_x2y, sum_xy, sum_y]

# Solve the system using Gaussian elimination
# Forward elimination
for i in range(3):
    # Find pivot
    max_row = i
    for k in range(i+1, 3):
        if abs(A[k][i]) > abs(A[max_row][i]):
            max_row = k
    A[i], A[max_row] = A[max_row], A[i]
    b[i], b[max_row] = b[max_row], b[i]
    
    # Make all rows below this one 0 in current column
    for k in range(i+1, 3):
        c = A[k][i] / A[i][i]
        for j in range(i, 3):
            if i == j:
                A[k][j] = 0
            else:
                A[k][j] -= c * A[i][j]
        b[k] -= c * b[i]

# Back substitution
solution = [0] * 3
for i in range(2, -1, -1):
    solution[i] = b[i]
    for j in range(i+1, 3):
        solution[i] -= A[i][j] * solution[j]
    solution[i] /= A[i][i]

# Output coefficients a, b, c
print(f"{solution[0]:.4f}")
print(f"{solution[1]:.4f}")
print(f"{solution[2]:.4f}")