import random

# Read input
line = input().strip()
samples, seed = map(int, line.split())

# Set the random seed
random.seed(seed)

# Monte Carlo simulation to estimate pi
inside_circle = 0

for _ in range(samples):
    # Generate random point in unit square [-1, 1] x [-1, 1]
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)
    
    # Check if point is inside unit circle
    if x*x + y*y <= 1:
        inside_circle += 1

# Estimate pi: ratio of points inside circle to total points, times 4
pi_estimate = 4 * inside_circle / samples

# Output to 6 decimal places
print(f"{pi_estimate:.6f}")