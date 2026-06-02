import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    coeffs = list(map(float, lines[0].split()))
    x0 = float(lines[1])
    learning_rate = float(lines[2])
    tolerance = float(lines[3])
    max_iters = int(lines[4])
    
    return coeffs, x0, learning_rate, tolerance, max_iters

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at x. Coefficients are in descending order of powers."""
    result = 0.0
    n = len(coeffs)
    for i, coeff in enumerate(coeffs):
        power = n - 1 - i
        result += coeff * (x ** power)
    return result

def evaluate_derivative(coeffs, x):
    """Evaluate derivative of polynomial at x."""
    result = 0.0
    n = len(coeffs)
    for i, coeff in enumerate(coeffs):
        power = n - 1 - i
        if power > 0:  # derivative of constant is 0
            result += coeff * power * (x ** (power - 1))
    return result

def gradient_descent():
    coeffs, x, learning_rate, tolerance, max_iters = read_input()
    
    for iteration in range(max_iters):
        f_x = evaluate_polynomial(coeffs, x)
        grad = evaluate_derivative(coeffs, x)
        
        print(f"Iter {iteration + 1}: x={x:.6f} f(x)={f_x:.6f} grad={grad:.6f}")
        
        if abs(grad) < tolerance:
            break
            
        x = x - learning_rate * grad
    
    final_f_x = evaluate_polynomial(coeffs, x)
    print(f"Minimum: x={x:.6f} f(x)={final_f_x:.6f}")

gradient_descent()