def de_casteljau(control_points, t):
    points = control_points[:]
    n = len(points)
    
    for i in range(1, n):
        for j in range(n - i):
            x = (1 - t) * points[j][0] + t * points[j + 1][0]
            y = (1 - t) * points[j][1] + t * points[j + 1][1]
            points[j] = (x, y)
    
    return points[0]

# Read input
degree = int(input())
control_points = []
for _ in range(degree + 1):
    x, y = map(float, input().split())
    control_points.append((x, y))
n = int(input())

# Generate N uniformly spaced parameter values
for i in range(n):
    t = i / (n - 1) if n > 1 else 0
    x, y = de_casteljau(control_points, t)
    print(f"{x:.4f} {y:.4f}")