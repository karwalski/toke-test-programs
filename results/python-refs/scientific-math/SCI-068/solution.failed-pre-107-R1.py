import sys

def solve_tridiagonal(a, b, c, d):
    """Solve tridiagonal system Ax = d where A has diagonals a, b, c"""
    n = len(d)
    if n == 0:
        return []
    if n == 1:
        return [d[0] / b[0]] if b[0] != 0 else [0]
    
    c_prime = [0] * n
    d_prime = [0] * n
    
    # Check bounds and avoid division by zero
    if len(b) > 0 and b[0] != 0:
        c_prime[0] = c[0] / b[0] if len(c) > 0 else 0
        d_prime[0] = d[0] / b[0]
    
    for i in range(1, n):
        # Add bounds checking
        a_val = a[i] if i < len(a) else 0
        b_val = b[i] if i < len(b) else 1
        c_val = c[i] if i < len(c) else 0
        
        denom = b_val - a_val * c_prime[i-1]
        if abs(denom) < 1e-10:
            denom = 1e-10
            
        if i < n-1:
            c_prime[i] = c_val / denom
        d_prime[i] = (d[i] - a_val * d_prime[i-1]) / denom
    
    x = [0] * n
    x[n-1] = d_prime[n-1]
    for i in range(n-2, -1, -1):
        x[i] = d_prime[i] - c_prime[i] * x[i+1]
    
    return x

def natural_cubic_spline(points, query_x):
    """Fit natural cubic spline and evaluate at query_x"""
    n = len(points)
    if n < 2:
        return 0
    
    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    
    # Calculate h values (intervals)
    h = []
    for i in range(n-1):
        h.append(x_vals[i+1] - x_vals[i])
    
    # Set up tridiagonal system for second derivatives
    # Natural spline: S''(x0) = S''(xn-1) = 0
    if n == 2:
        # Linear case
        m = [0, 0]
    else:
        # Build tridiagonal matrix for interior points
        # For natural spline, we solve for m[1] to m[n-2] (interior points)
        # with m[0] = m[n-1] = 0
        interior_n = n - 2
        if interior_n <= 0:
            m = [0] * n
        else:
            a = []  # sub-diagonal
            b = []  # main diagonal  
            c = []  # super-diagonal
            d = []  # right hand side
            
            for i in range(interior_n):
                actual_i = i + 1  # actual index in original points
                
                # Sub-diagonal
                if i == 0:
                    a.append(0)
                else:
                    a.append(h[actual_i-1])
                
                # Main diagonal
                b.append(2 * (h[actual_i-1] + h[actual_i]))
                
                # Super-diagonal
                if i == interior_n - 1:
                    c.append(0)
                else:
                    c.append(h[actual_i])
                
                # Right hand side
                d.append(6 * ((y_vals[actual_i+1] - y_vals[actual_i]) / h[actual_i] - 
                             (y_vals[actual_i] - y_vals[actual_i-1]) / h[actual_i-1]))
            
            # Solve for interior second derivatives
            m_interior = solve_tridiagonal(a, b, c, d)
            
            # Construct full m array
            m = [0] + m_interior + [0]
    
    # Find which interval contains query_x
    for i in range(n-1):
        if x_vals[i] <= query_x <= x_vals[i+1]:
            # Calculate spline value in interval [x_i, x_{i+1}]
            dx = x_vals[i+1] - x_vals[i]
            if abs(dx) < 1e-10:
                return y_vals[i]
                
            a_coeff = (m[i+1] - m[i]) / (6 * dx)
            b_coeff = m[i] / 2
            c_coeff = (y_vals[i+1] - y_vals[i]) / dx - dx * (2 * m[i] + m[i+1]) / 6
            d_coeff = y_vals[i]
            
            t = query_x - x_vals[i]
            result = a_coeff * t**3 + b_coeff * t**2 + c_coeff * t + d_coeff
            return result
    
    # If query_x is outside range, return nearest endpoint
    if query_x < x_vals[0]:
        return y_vals[0]
    else:
        return y_vals[-1]

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

if len(lines) < 1:
    sys.exit(1)

try:
    n = int(lines[0])
    
    if len(lines) < n + 1:
        sys.exit(1)
    
    points = []
    for i in range(1, n + 1):
        if i < len(lines):
            x, y = map(float, lines[i].split())
            points.append((x, y))
    
    # Process query points
    for i in range(n + 1, len(lines)):
        if lines[i].strip():
            query_x = float(lines[i])
            result = natural_cubic_spline(points, query_x)
            print(f"S({query_x}) = {result:.6f}")

except (ValueError, IndexError):
    sys.exit(1)