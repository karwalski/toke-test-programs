import math
import sys

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    n = int(lines[0])
    points = []
    for i in range(1, n + 1):
        x, y = map(float, lines[i].split())
        points.append((x, y))
    start = int(lines[n + 1])
    return n, points, start

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def nearest_neighbor_tsp(points, start):
    n = len(points)
    visited = [False] * n
    route = [start]
    visited[start] = True
    current = start
    total_distance = 0
    
    for _ in range(n - 1):
        min_dist = float('inf')
        next_city = -1
        
        for i in range(n):
            if not visited[i]:
                dist = distance(points[current], points[i])
                if dist < min_dist:
                    min_dist = dist
                    next_city = i
        
        route.append(next_city)
        visited[next_city] = True
        total_distance += min_dist
        current = next_city
    
    # Return to start
    route.append(start)
    total_distance += distance(points[current], points[start])
    
    return route, total_distance

def calculate_lower_bound(points):
    # Simple lower bound: minimum spanning tree approximation
    # Using the sum of the two shortest edges from each vertex divided by 2
    n = len(points)
    total = 0
    
    for i in range(n):
        distances = []
        for j in range(n):
            if i != j:
                distances.append(distance(points[i], points[j]))
        distances.sort()
        # Take the two shortest edges from each vertex
        total += distances[0] + distances[1]
    
    return total / 2

def main():
    n, points, start = read_input()
    route, total_distance = nearest_neighbor_tsp(points, start)
    lower_bound = calculate_lower_bound(points)
    approximation_ratio = total_distance / lower_bound
    
    route_str = " ".join(map(str, route))
    print(f"Route: {route_str}")
    print(f"Total distance: {total_distance:.4f}")
    print(f"Approximation ratio: {approximation_ratio:.2f}")

if __name__ == "__main__":
    main()