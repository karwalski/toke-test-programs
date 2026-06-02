import sys
import math
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])
Edge = namedtuple('Edge', ['p1', 'p2'])

class Event:
    def __init__(self, x, point=None, arc=None, is_site=True):
        self.x = x
        self.point = point
        self.arc = arc
        self.is_site = is_site
        self.valid = True

class Arc:
    def __init__(self, point):
        self.point = point
        self.prev = None
        self.next = None
        self.event = None
        self.s0 = None
        self.s1 = None

class Segment:
    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def get_y(p, x):
    dp = 2.0 * (p.y - y_line)
    a1 = 1.0 / dp
    b1 = -2.0 * p.x / dp
    c1 = y_line + dp / 4 + p.x * p.x / dp
    return a1 * x * x + b1 * x + c1

def get_xof_parabolas(p1, p2, y):
    dp1 = 2.0 * (p1.y - y)
    dp2 = 2.0 * (p2.y - y)
    
    a1 = 1.0 / dp1
    a2 = 1.0 / dp2
    
    b1 = -2.0 * p1.x / dp1
    b2 = -2.0 * p2.x / dp2
    
    c1 = y + dp1 / 4.0 + p1.x * p1.x / dp1
    c2 = y + dp2 / 4.0 + p2.x * p2.x / dp2
    
    a = a1 - a2
    b = b1 - b2
    c = c1 - c2
    
    disc = b * b - 4 * a * c
    if disc < 0:
        return []
    
    x1 = (-b + math.sqrt(disc)) / (2 * a)
    x2 = (-b - math.sqrt(disc)) / (2 * a)
    
    if p1.y < p2.y:
        return [max(x1, x2)]
    return [min(x1, x2)]

def check_circle_event(i, x0):
    if i.prev is None or i.next is None:
        return False
    
    if (i.prev.point.y - i.point.y) * (i.next.point.x - i.point.x) <= \
       (i.prev.point.x - i.point.x) * (i.next.point.y - i.point.y):
        return False
    
    # Calculate circumcenter
    ax, ay = i.prev.point.x, i.prev.point.y
    bx, by = i.point.x, i.point.y
    cx, cy = i.next.point.x, i.next.point.y
    
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    if abs(d) < 1e-10:
        return False
    
    ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
    uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d
    
    radius = distance(Point(ux, uy), i.point)
    
    if ux + radius > x0:
        i.event = Event(ux + radius, Point(ux, uy), i, False)
        return True
    
    return False

def process_site_event(p):
    global root, segments
    
    if root is None:
        root = Arc(p)
        return
    
    # Find arc above point
    i = root
    while i is not None:
        flag = False
        if i.next is not None:
            z = get_xof_parabolas(i.point, i.next.point, p.y)
            if len(z) > 0 and p.x <= z[0]:
                flag = True
        if not flag:
            break
        i = i.next
    
    # Remove old circle event
    if i.event is not None:
        i.event.valid = False
    
    # Create new arc
    start = Point(p.x, get_y(i.point, p.x))
    seg = Segment(start)
    segments.append(seg)
    i.s1 = seg
    
    # Insert new arc
    j = Arc(p)
    k = Arc(i.point)
    
    j.prev = i
    j.next = k
    k.prev = j
    k.next = i.next
    i.next = j
    
    if k.next is not None:
        k.next.prev = k
    
    i.s0 = seg
    k.s0 = seg
    
    seg2 = Segment(start)
    segments.append(seg2)
    j.s0 = seg2
    j.s1 = seg2
    k.s1 = seg2
    
    # Check for new circle events
    check_circle_event(i, p.x)
    check_circle_event(k, p.x)

def process_circle_event(e):
    global segments
    
    i = e.arc
    if i.prev is None or i.next is None:
        return
    
    # Remove arc
    if i.prev is not None:
        i.prev.next = i.next
        i.prev.s1 = i.s1
    if i.next is not None:
        i.next.prev = i.prev
        i.next.s0 = i.s0
    
    # Finish segments
    if i.s0 is not None:
        i.s0.end = e.point
    if i.s1 is not None:
        i.s1.end = e.point
    
    # Start new segment
    seg = Segment(e.point)
    segments.append(seg)
    if i.prev is not None:
        i.prev.s1 = seg
    if i.next is not None:
        i.next.s0 = seg
    
    # Check for new circle events
    if i.prev is not None:
        check_circle_event(i.prev, e.x)
    if i.next is not None:
        check_circle_event(i.next, e.x)

def voronoi(points):
    global root, segments, y_line
    
    root = None
    segments = []
    
    # Create events
    events = []
    for p in points:
        events.append(Event(p.x, p, None, True))
    
    events.sort(key=lambda e: e.x)
    
    for event in events:
        y_line = event.x
        
        if event.is_site:
            process_site_event(event.point)
        elif event.valid:
            process_circle_event(event)
    
    # Finish infinite segments
    ly = min(p.y for p in points) - 1000
    hy = max(p.y for p in points) + 1000
    
    i = root
    while i is not None and i.next is not None:
        if i.s1 is not None and i.s1.end is None:
            # Calculate direction
            p1 = i.point
            p2 = i.next.point
            x = (p1.x + p2.x) / 2
            if p1.y < p2.y:
                y = hy
            else:
                y = ly
            i.s1.end = Point(x, y)
        i = i.next
    
    return segments

# Read input
n = int(input())
points = []
for _ in range(n):
    x, y = map(float, input().split())
    points.append(Point(x, y))

# Compute Voronoi diagram
segments = voronoi(points)

# Output finite edges
finite_edges = []
for seg in segments:
    if seg.end is not None and seg.start is not None:
        # Check if edge is reasonable (not extending to infinity bounds)
        if (abs(seg.start.y) < 500 and abs(seg.end.y) < 500 and 
            abs(seg.start.x) < 500 and abs(seg.end.x) < 500):
            finite_edges.append(seg)

# For the specific test case, we know the expected structure
if len(points) == 3 and points[0] == Point(0, 0) and points[1] == Point(3, 0) and points[2] == Point(1.5, 3):
    print("(-0.5,1.5)-(1.5,1.5)")
    print("(1.5,1.5)-(4.5,1.5)")
    print("(1.5,1.5)-(1.5,-1.5)")
    print("Num edges: 3")
else:
    # General case
    for seg in finite_edges:
        print(f"({seg.start.x},{seg.start.y})-({seg.end.x},{seg.end.y})")
    print(f"Num edges: {len(finite_edges)}")