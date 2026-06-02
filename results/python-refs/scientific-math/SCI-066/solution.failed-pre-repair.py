import sys

def lagrange_interpolation(data_points, x):
    n = len(data_points)
    result = 0.0
    
    for i in range(n):
        xi, yi = data_points[i]
        
        # Calculate L_i(x)
        li = 1.0
        for j in range(n):
            if i != j:
                xj, _ = data_points[j]
                li *= (x - xj) / (xi - xj)
        
        result += yi * li
    
    return result

# Read input
lines = []
for line in sys.stdin:
    lines.append(line.strip())

n = int(lines[0])

# Read data points
data_points = []
for i in range(1, n + 1):
    x, y = map(float, lines[i].split())
    data_points.append((x, y))

# Process query points
for i in range(n + 1, len(lines)):
    query_x = float(lines[i])
    result = lagrange_interpolation(data_points, query_x)
    print(f"p({query_x}) = {result:.6f}")