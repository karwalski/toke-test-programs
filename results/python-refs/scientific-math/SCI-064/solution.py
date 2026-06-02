import sys

# Read coefficients from first line
coeffs = list(map(float, input().split()))

# Read x values from remaining lines
for line in sys.stdin:
    x = float(line.strip())
    
    # Horner's method: start with highest degree coefficient
    # For c0 + c1*x + c2*x^2 + ..., we work backwards
    result = 0
    for i in range(len(coeffs) - 1, -1, -1):
        result = result * x + coeffs[i]
    
    print(f"p({x:g}) = {result:.6f}")