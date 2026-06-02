import sys

def line_segment_intersection():
    # Read input
    line1 = list(map(float, input().split()))
    line2 = list(map(float, input().split()))
    
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2
    
    # Calculate direction vectors
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3
    
    # Calculate the denominator (cross product of direction vectors)
    denominator = dx1 * dy2 - dy1 * dx2
    
    # Check if lines are parallel
    if abs(denominator) < 1e-10:
        # Lines are parallel, check if they are collinear
        # Vector from point on line 1 to point on line 2
        dx3 = x3 - x1
        dy3 = y3 - y1
        
        # Check if point (x3, y3) lies on the line defined by segment 1
        cross_product = dx1 * dy3 - dy1 * dx3
        
        if abs(cross_product) < 1e-10:
            print("COLLINEAR")
        else:
            print("PARALLEL")
        return
    
    # Calculate parameters t and u
    dx3 = x3 - x1
    dy3 = y3 - y1
    
    t = (dx3 * dy2 - dy3 * dx2) / denominator
    u = (dx3 * dy1 - dy3 * dx1) / denominator
    
    # Check if intersection point lies within both segments
    if 0 <= t <= 1 and 0 <= u <= 1:
        # Calculate intersection point
        ix = x1 + t * dx1
        iy = y1 + t * dy1
        print(f"INTERSECT at ({ix:.6f}, {iy:.6f})")
    else:
        print("NO INTERSECT")

line_segment_intersection()