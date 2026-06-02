import sys

def polynomial(x, coefficients):
    result = 0
    for i, coeff in enumerate(coefficients):
        result += coeff * (x ** i)
    return result

def simpsons_rule(a, b, n, coefficients):
    h = (b - a) / n
    
    # Calculate f(x0) + f(xn)
    result = polynomial(a, coefficients) + polynomial(b, coefficients)
    
    # Calculate sum of f(x_odd) * 4
    for i in range(1, n, 2):
        x = a + i * h
        result += 4 * polynomial(x, coefficients)
    
    # Calculate sum of f(x_even) * 2
    for i in range(2, n, 2):
        x = a + i * h
        result += 2 * polynomial(x, coefficients)
    
    # Multiply by h/3
    result *= h / 3
    
    return result

# Read input
a = float(input().strip())
b = float(input().strip())
n = int(input().strip())
coefficients = list(map(float, input().strip().split()))

# Calculate integral using Simpson's rule
integral = simpsons_rule(a, b, n, coefficients)

# Output result
print(f"Integral: {integral:.6f}")