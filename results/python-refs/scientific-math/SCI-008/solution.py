import math

# Read input
line1 = input().split()
x0, y0 = float(line1[0]), float(line1[1])
x_end = float(input())
h = float(input())
expression = input().strip()

# Define the function f(x,y) from the expression
def f(x, y):
    # Replace variables in expression and evaluate
    expr = expression.replace('x', str(x)).replace('y', str(y))
    # Handle mathematical functions
    expr = expr.replace('sin', 'math.sin')
    expr = expr.replace('cos', 'math.cos')
    expr = expr.replace('tan', 'math.tan')
    expr = expr.replace('exp', 'math.exp')
    expr = expr.replace('log', 'math.log')
    expr = expr.replace('sqrt', 'math.sqrt')
    return eval(expr)

# Initialize
x = x0
y = y0

# Output initial point
print(f"{x:.6f} {y:.6f}")

# Runge-Kutta 4th order method
while x < x_end - h/2:  # Use h/2 to avoid floating point precision issues
    k1 = h * f(x, y)
    k2 = h * f(x + h/2, y + k1/2)
    k3 = h * f(x + h/2, y + k2/2)
    k4 = h * f(x + h, y + k3)
    
    y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
    x = x + h
    
    print(f"{x:.6f} {y:.6f}")