def evaluate_polynomial(coefficients, x):
    """Evaluate polynomial at x using Horner's method"""
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result

def evaluate_derivative(coefficients, x):
    """Evaluate derivative of polynomial at x"""
    if len(coefficients) <= 1:
        return 0
    
    # Derivative coefficients
    derivative_coeffs = []
    for i in range(len(coefficients) - 1):
        derivative_coeffs.append(coefficients[i] * (len(coefficients) - 1 - i))
    
    return evaluate_polynomial(derivative_coeffs, x)

def newton_method(initial_guess, tolerance, max_iterations, coefficients):
    """Find root using Newton's method"""
    x = initial_guess
    
    for iteration in range(max_iterations):
        f_x = evaluate_polynomial(coefficients, x)
        
        # Check if we found the root
        if abs(f_x) < tolerance:
            return x, iteration + 1
        
        f_prime_x = evaluate_derivative(coefficients, x)
        
        # Check for zero derivative
        if abs(f_prime_x) < 1e-15:
            break
        
        # Newton's method update
        x_new = x - f_x / f_prime_x
        
        # Check convergence
        if abs(x_new - x) < tolerance:
            return x_new, iteration + 1
        
        x = x_new
    
    return x, max_iterations

# Read input
line1 = input().strip().split()
initial_guess = float(line1[0])
tolerance = float(line1[1])
max_iterations = int(line1[2])

line2 = input().strip().split()
coefficients = [float(x) for x in line2]

# Find root using Newton's method
root, iterations = newton_method(initial_guess, tolerance, max_iterations, coefficients)

# Output result
print(f"{root:.6f}")
print(f"{iterations} iterations")