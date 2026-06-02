import sys

def orientation(p, q, r):
    """Find orientation of ordered triplet (p, q, r).
    Returns:
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def jarvis_march(points):
    n = len(points)
    if n < 3:
        return points
    
    # Find the leftmost point
    leftmost = 0
    for i in range(1, n):
        if points[i][0] < points[leftmost][0]:
            leftmost = i
        elif points[i][0] == points[leftmost][0] and points[i][1] < points[leftmost][1]:
            leftmost = i
    
    hull = []
    p = leftmost
    
    while True:
        hull.append(points[p])
        
        # Find the most counterclockwise point from points[p]
        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i
        
        p = q
        
        # If we come back to start point, we have completed the hull
        if p == leftmost:
            break
    
    return hull

# Read input
n = int(input())
points = []
for _ in range(n):
    x, y = map(float, input().split())
    points.append((x, y))

# Compute convex hull
hull = jarvis_march(points)

# Format output
hull_str = ""
for i, point in enumerate(hull):
    if i > 0:
        hull_str += " "
    # Format numbers to remove unnecessary decimals
    x_str = str(int(point[0])) if point[0] == int(point[0]) else str(point[0])
    y_str = str(int(point[1])) if point[1] == int(point[1]) else str(point[1])
    hull_str += f"({x_str},{y_str})"

print(f"Hull points: {hull_str}")
print(f"Hull size: {len(hull)} points")