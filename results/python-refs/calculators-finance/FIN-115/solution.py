import sys

# Read input
line1 = input().strip().split()
lower = float(line1[0])
upper = float(line1[1])
num_trapezoids = int(line1[2])

line2 = input().strip().split()
coefficients = [float(x) for x in line2]

def evaluate_polynomial(x, coeffs):
    result = 0
    degree = len(coeffs) - 1
    for i, coeff in enumerate(coeffs):
        power = degree - i
        result += coeff * (x ** power)
    return result

# Trapezoidal rule
h = (upper - lower) / num_trapezoids
integral = 0

for i in range(num_trapezoids):
    x0 = lower + i * h
    x1 = lower + (i + 1) * h
    y0 = evaluate_polynomial(x0, coefficients)
    y1 = evaluate_polynomial(x1, coefficients)
    integral += (y0 + y1) * h / 2

print(f"{integral:.4f}")