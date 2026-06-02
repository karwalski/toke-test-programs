import math

n = int(input())
vertices = []
for _ in range(n):
    x, y = map(float, input().split())
    vertices.append((x, y))

# Compute area using shoelace formula
area = 0
for i in range(n):
    j = (i + 1) % n
    area += vertices[i][0] * vertices[j][1]
    area -= vertices[j][0] * vertices[i][1]
area = abs(area) / 2

# Compute perimeter
perimeter = 0
for i in range(n):
    j = (i + 1) % n
    dx = vertices[j][0] - vertices[i][0]
    dy = vertices[j][1] - vertices[i][1]
    perimeter += math.sqrt(dx * dx + dy * dy)

# Determine winding (using signed area)
signed_area = 0
for i in range(n):
    j = (i + 1) % n
    signed_area += vertices[i][0] * vertices[j][1]
    signed_area -= vertices[j][0] * vertices[i][1]

winding = "CCW" if signed_area > 0 else "CW"

print(f"Area: {area:.6f}")
print(f"Perimeter: {perimeter:.6f}")
print(f"Winding: {winding}")