def evaluate_polynomial(coeffs, x):
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result

def trapezoidal_rule(a, b, n, coeffs):
    h = (b - a) / n
    
    # Calculate f(a)
    fa = evaluate_polynomial(coeffs, a)
    
    # Calculate f(b)
    fb = evaluate_polynomial(coeffs, b)
    
    # Calculate sum of f(xi) for i = 1 to n-1
    sum_middle = 0
    for i in range(1, n):
        xi = a + i * h
        sum_middle += evaluate_polynomial(coeffs, xi)
    
    # Apply trapezoidal rule
    integral = h * (fa + 2 * sum_middle + fb) / 2
    return integral

# Read input
a = float(input())
b = float(input())
n = int(input())
coeffs = list(map(float, input().split()))

# Calculate integral
result = trapezoidal_rule(a, b, n, coeffs)

# Output result
print(f"Integral: {result:.6f}")