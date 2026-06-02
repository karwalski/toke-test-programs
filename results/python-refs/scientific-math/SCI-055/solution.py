import sys

def point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    
    # First check if point is on boundary
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]
        
        # Check if point is on edge
        if is_on_segment(x, y, x1, y1, x2, y2):
            return "BOUNDARY"
    
    # Ray casting algorithm for inside/outside
    inside = False
    j = n - 1
    
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    
    return "INSIDE" if inside else "OUTSIDE"

def is_on_segment(px, py, x1, y1, x2, y2):
    # Check if point (px, py) lies on line segment from (x1, y1) to (x2, y2)
    
    # Check if point is within bounding box
    if not (min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)):
        return False
    
    # Check if point is collinear with the segment
    # Using cross product: (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1) == 0
    cross_product = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    
    # Use small epsilon for floating point comparison
    return abs(cross_product) < 1e-10

# Read input
n = int(input())
polygon = []
for _ in range(n):
    x, y = map(float, input().split())
    polygon.append((x, y))

q = int(input())
for _ in range(q):
    x, y = map(float, input().split())
    result = point_in_polygon((x, y), polygon)
    print(result)