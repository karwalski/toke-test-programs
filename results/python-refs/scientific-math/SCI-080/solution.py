import sys
import math
from itertools import permutations

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)

def calculate_route_distance(cities, route):
    total_dist = 0
    for i in range(len(route)):
        from_city = cities[route[i]]
        to_city = cities[route[(i + 1) % len(route)]]
        total_dist += distance(from_city, to_city)
    return total_dist

# Read input
n = int(input())
cities = []
for _ in range(n):
    x, y = map(int, input().split())
    cities.append((x, y))

# Generate all possible routes (permutations starting from city 0)
min_distance = float('inf')
best_route = None

# Fix the starting city as 0 to avoid duplicate rotations
remaining_cities = list(range(1, n))
for perm in permutations(remaining_cities):
    route = [0] + list(perm)
    dist = calculate_route_distance(cities, route)
    if dist < min_distance:
        min_distance = dist
        best_route = route

# Output the result
route_str = ' '.join(map(str, best_route + [best_route[0]]))
print(f"Optimal route: {route_str}")
print(f"Total distance: {min_distance:.4f}")