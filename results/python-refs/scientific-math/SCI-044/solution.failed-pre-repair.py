import sys

# Read input
coeffs = list(map(float, input().split()))
a, b = map(float, input().split())
tolerance = float(input())
max_iterations = int(input())

# Define polynomial function
def f(x):
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** (len(coeffs) - 1 - i))
    return result

# Bisection method
iteration = 0
left, right = a, b

for iteration in range(1, max_iterations + 1):
    mid = (left + right) / 2
    f_mid = f(mid)
    
    print(f"Iteration {iteration}: [{left},{right}] midpoint={mid} f(mid)={f_mid}")
    
    if abs(f_mid) < tolerance or (right - left) / 2 < tolerance:
        break
    
    if f(left) * f_mid < 0:
        right = mid
    else:
        left = mid

# Final result
final_root = (left + right) / 2
print(f"Root: {final_root:.6f} ({iteration} iterations)")