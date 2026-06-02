import sys

# Read input
line1 = input().strip().split()
x0, y0 = float(line1[0]), float(line1[1])
x_end = float(input().strip())
h = float(input().strip())
expression = input().strip()

# Initialize variables
x, y = x0, y0

# Print initial condition
print(f"{x:.6f} {y:.6f}")

# Euler method
while x < x_end:
    # Calculate dy/dx using the expression
    # Replace 'x' and 'y' in the expression with their current values
    dydx = eval(expression, {"x": x, "y": y})
    
    # Update y using Euler's method: y_new = y_old + h * dy/dx
    y = y + h * dydx
    
    # Update x
    x = x + h
    
    # Print current step
    print(f"{x:.6f} {y:.6f}")