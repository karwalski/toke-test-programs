import random
import math

# Read number of points
N = int(input())

# Initialize counter for points inside circle
points_inside = 0

# Generate N random points and check if they're inside the unit circle
for _ in range(N):
    x = random.random()  # Random float between 0 and 1
    y = random.random()  # Random float between 0 and 1
    
    # Check if point is inside unit circle (x^2 + y^2 <= 1)
    if x*x + y*y <= 1:
        points_inside += 1

# Estimate pi: pi/4 = (points inside circle) / (total points)
# So pi = 4 * (points inside circle) / (total points)
pi_estimate = 4 * points_inside / N

# Calculate error percentage
actual_pi = math.pi
error_percent = abs(pi_estimate - actual_pi) / actual_pi * 100

# Print results in the required format
print(f"Points inside circle: {points_inside}")
print(f"Estimate of pi: {pi_estimate:.6f}")
print(f"Error: {error_percent:.6f}%")