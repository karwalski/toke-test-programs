import random
import math

def simulate_random_walk(steps):
    x, y = 0, 0
    max_distance = 0
    
    for _ in range(steps):
        # Move in one of 4 directions: up, down, left, right
        direction = random.randint(0, 3)
        if direction == 0:    # up
            y += 1
        elif direction == 1:  # down
            y -= 1
        elif direction == 2:  # left
            x -= 1
        else:                 # right
            x += 1
        
        # Calculate current distance from origin
        current_distance = math.sqrt(x*x + y*y)
        max_distance = max(max_distance, current_distance)
    
    # Final distance from origin
    final_distance = math.sqrt(x*x + y*y)
    
    return final_distance, max_distance

# Read input
steps = int(input().strip())
trials = int(input().strip())

# Run simulations
total_final_distance = 0
total_max_distance = 0

for _ in range(trials):
    final_dist, max_dist = simulate_random_walk(steps)
    total_final_distance += final_dist
    total_max_distance += max_dist

# Calculate means
mean_final_distance = total_final_distance / trials
mean_max_distance = total_max_distance / trials

# Expected RMS for 2D random walk is sqrt(steps)
expected_rms = math.sqrt(steps)

# Output results
print(f"Mean final distance: {mean_final_distance:.2f}")
print(f"Mean max distance: {mean_max_distance:.2f}")
print(f"Expected RMS: {expected_rms:.2f}")