import math

def cross_product(O, A, B):
    return (A[0] - O[0]) * (B[1] - O[1]) - (A[1] - O[1]) * (B[0] - O[0])

def distance_squared(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

def polar_angle(p0, p):
    return math.atan2(p[1] - p0[1], p[0] - p0[0])

def graham_scan(points):
    n = len(points)
    if n < 3:
        return points
    
    # Find the bottom-most point (or left most in case of tie)
    start = min(points, key=lambda p: (p[1], p[0]))
    
    # Sort points by polar angle with respect to start point
    def compare_points(p):
        angle = polar_angle(start, p)
        dist = distance_squared(start, p)
        return (angle, dist)
    
    other_points = [p for p in points if p != start]
    other_points.sort(key=compare_points)
    
    # Build convex hull
    hull = [start]
    
    for p in other_points:
        # Remove points that make clockwise turn
        while len(hull) > 1 and cross_product(hull[-2], hull[-1], p) < 0:
            hull.pop()
        hull.append(p)
    
    return hull

def polygon_area(points):
    n = len(points)
    if n < 3:
        return 0.0
    
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    
    return abs(area) / 2.0

# Read input
n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append((x, y))

# Compute convex hull
hull = graham_scan(points)

# Output hull points
hull_str = " ".join(f"({x},{y})" for x, y in hull)
print(f"Hull points: {hull_str}")

# Compute and output area
area = polygon_area(hull)
print(f"Hull area: {area:.6f}")