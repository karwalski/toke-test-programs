import math
import sys

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def brute_force(points):
    min_dist = float('inf')
    closest_pair = None
    n = len(points)
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (points[i], points[j])
    
    return closest_pair, min_dist

def closest_pair_rec(px, py):
    n = len(px)
    
    # Base case: use brute force for small arrays
    if n <= 3:
        return brute_force(px)
    
    # Divide
    mid = n // 2
    midpoint = px[mid]
    
    pyl = [point for point in py if point[0] <= midpoint[0]]
    pyr = [point for point in py if point[0] > midpoint[0]]
    
    # Conquer
    (p1_left, p2_left), dist_left = closest_pair_rec(px[:mid], pyl)
    (p1_right, p2_right), dist_right = closest_pair_rec(px[mid:], pyr)
    
    # Find minimum of the two halves
    if dist_left <= dist_right:
        min_dist = dist_left
        closest_pair = (p1_left, p2_left)
    else:
        min_dist = dist_right
        closest_pair = (p1_right, p2_right)
    
    # Check points near the dividing line
    strip = [point for point in py if abs(point[0] - midpoint[0]) < min_dist]
    
    for i in range(len(strip)):
        j = i + 1
        while j < len(strip) and (strip[j][1] - strip[i][1]) < min_dist:
            dist = distance(strip[i], strip[j])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (strip[i], strip[j])
            j += 1
    
    return closest_pair, min_dist

def closest_pair(points):
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    return closest_pair_rec(px, py)

# Read input
n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append((x, y))

# Find closest pair
(p1, p2), dist = closest_pair(points)

# Output
print(f"Closest pair: ({p1[0]},{p1[1]}) and ({p2[0]},{p2[1]})")
print(f"Distance: {dist:.6f}")