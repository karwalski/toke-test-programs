import sys
import math

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at x using Horner's method"""
    result = 0
    for coeff in coeffs:
        result = result * x + coeff
    return result

def evaluate_derivative(coeffs, x):
    """Evaluate derivative of polynomial at x"""
    if len(coeffs) <= 1:
        return 0
    
    # Derivative coefficients
    deriv_coeffs = []
    degree = len(coeffs) - 1
    for i in range(len(coeffs) - 1):
        deriv_coeffs.append(coeffs[i] * (degree - i))
    
    return evaluate_polynomial(deriv_coeffs, x)

def newton_method(coeffs, start_x, max_iter=100, tolerance=1e-10):
    """Find root using Newton's method starting from start_x"""
    x = start_x
    
    for _ in range(max_iter):
        f_x = evaluate_polynomial(coeffs, x)
        
        if abs(f_x) < tolerance:
            return x
            
        f_prime_x = evaluate_derivative(coeffs, x)
        
        if abs(f_prime_x) < tolerance:
            return None  # Derivative too close to zero
            
        x_new = x - f_x / f_prime_x
        
        if abs(x_new - x) < tolerance:
            return x_new
            
        x = x_new
    
    return None

def find_all_roots(coeffs):
    """Find all real roots by trying multiple starting points"""
    roots = []
    
    # Try various starting points
    start_points = []
    
    # Add points around potential roots based on coefficient ratios
    for i in range(-20, 21):
        start_points.append(float(i))
    
    # Add some fractional starting points
    for i in range(-40, 41):
        start_points.append(i * 0.5)
    
    for start in start_points:
        root = newton_method(coeffs, start)
        
        if root is not None:
            # Verify this is actually a root
            if abs(evaluate_polynomial(coeffs, root)) < 1e-8:
                # Check if we already found this root
                is_duplicate = False
                for existing_root in roots:
                    if abs(root - existing_root) < 1e-6:
                        is_duplicate = True
                        break
                
                if not is_duplicate:
                    roots.append(root)
    
    return sorted(roots)

# Read input
line = input().strip()
coeffs = list(map(float, line.split()))

# Find roots
roots = find_all_roots(coeffs)

# Output results
if not roots:
    print("No real roots")
else:
    for root in roots:
        print(f"{root:.4f}")