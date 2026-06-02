import sys

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at x"""
    result = 0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result

def evaluate_derivative(coeffs, x):
    """Evaluate derivative of polynomial at x"""
    result = 0
    for i in range(1, len(coeffs)):
        result += i * coeffs[i] * (x ** (i-1))
    return result

# Read input
coeffs = list(map(float, input().split()))
x0 = float(input())
tolerance = float(input())
max_iterations = int(input())

x = x0
for iteration in range(1, max_iterations + 1):
    f_x = evaluate_polynomial(coeffs, x)
    f_prime_x = evaluate_derivative(coeffs, x)
    
    print(f"Iteration {iteration}: x={x:.6f} f(x)={f_x:.6f}")
    
    # Check for convergence
    if abs(f_x) < tolerance:
        print(f"Root: {x:.6f} ({iteration} iterations)")
        break
    
    # Check if derivative is zero (would cause division by zero)
    if abs(f_prime_x) < 1e-15:
        print(f"Root: {x:.6f} ({iteration} iterations)")
        break
    
    # Newton-Raphson update
    x_new = x - f_x / f_prime_x
    
    # Check if we've reached the maximum iterations
    if iteration == max_iterations:
        print(f"Root: {x_new:.6f} ({iteration} iterations)")
        break
    
    x = x_new