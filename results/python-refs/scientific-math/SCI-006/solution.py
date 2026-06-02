import math

def gauss_legendre_nodes_weights(n):
    """Generate Gauss-Legendre nodes and weights for n points"""
    if n == 2:
        nodes = [-1/math.sqrt(3), 1/math.sqrt(3)]
        weights = [1.0, 1.0]
    elif n == 3:
        nodes = [-math.sqrt(3/5), 0, math.sqrt(3/5)]
        weights = [5/9, 8/9, 5/9]
    elif n == 4:
        nodes = [-math.sqrt((3+2*math.sqrt(6/5))/7), -math.sqrt((3-2*math.sqrt(6/5))/7), 
                 math.sqrt((3-2*math.sqrt(6/5))/7), math.sqrt((3+2*math.sqrt(6/5))/7)]
        weights = [(18-math.sqrt(30))/36, (18+math.sqrt(30))/36, 
                  (18+math.sqrt(30))/36, (18-math.sqrt(30))/36]
    elif n == 5:
        nodes = [-math.sqrt(5+2*math.sqrt(10/7))/3, -math.sqrt(5-2*math.sqrt(10/7))/3, 0,
                 math.sqrt(5-2*math.sqrt(10/7))/3, math.sqrt(5+2*math.sqrt(10/7))/3]
        weights = [(322-13*math.sqrt(70))/900, (322+13*math.sqrt(70))/900, 128/225,
                  (322+13*math.sqrt(70))/900, (322-13*math.sqrt(70))/900]
    else:
        # Use iterative method for other values of n
        nodes = []
        weights = []
        
        for i in range(1, n + 1):
            # Initial guess for the i-th root
            x = math.cos(math.pi * (i - 0.25) / (n + 0.5))
            
            # Newton-Raphson iteration
            for _ in range(20):
                p1 = 1.0
                p2 = 0.0
                
                # Evaluate Legendre polynomial at x
                for j in range(1, n + 1):
                    p3 = p2
                    p2 = p1
                    p1 = ((2 * j - 1) * x * p2 - (j - 1) * p3) / j
                
                # Evaluate derivative
                pp = n * (x * p1 - p2) / (x * x - 1)
                
                x1 = x
                x = x1 - p1 / pp
                
                if abs(x - x1) < 1e-14:
                    break
            
            nodes.append(x)
            weights.append(2.0 / ((1 - x * x) * pp * pp))
    
    return nodes, weights

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at x given coefficients [a0, a1, a2, ...] for a0 + a1*x + a2*x^2 + ..."""
    result = 0.0
    for i, coeff in enumerate(coeffs):
        result += coeff * (x ** i)
    return result

# Read input
a = float(input().strip())
b = float(input().strip())
n_points = int(input().strip())
coeffs = list(map(float, input().strip().split()))

# Get Gauss-Legendre nodes and weights
nodes, weights = gauss_legendre_nodes_weights(n_points)

# Transform nodes from [-1, 1] to [a, b]
transformed_nodes = [(b - a) / 2 * node + (a + b) / 2 for node in nodes]

# Compute the integral
integral = 0.0
for i in range(n_points):
    x = transformed_nodes[i]
    fx = evaluate_polynomial(coeffs, x)
    integral += weights[i] * fx

# Scale by the transformation factor
integral *= (b - a) / 2

print(f"Integral: {integral:.6f}")