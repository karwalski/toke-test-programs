import random
import math

# Read input
steps = int(input())
trials = int(input())

total_final_position = 0
total_max_displacement = 0
total_returns_to_zero = 0

for trial in range(trials):
    position = 0
    max_displacement = 0
    returns_to_zero = 0
    
    for step in range(steps):
        # Random step: +1 or -1
        position += 1 if random.random() < 0.5 else -1
        
        # Track maximum displacement from origin
        max_displacement = max(max_displacement, abs(position))
        
        # Count returns to origin
        if position == 0:
            returns_to_zero += 1
    
    total_final_position += position
    total_max_displacement += max_displacement
    total_returns_to_zero += returns_to_zero

# Calculate means
mean_final_position = total_final_position / trials
mean_max_displacement = total_max_displacement / trials
mean_returns_to_zero = total_returns_to_zero / trials
expected_rms = math.sqrt(steps)

# Output results
print(f"Mean final position: {mean_final_position:.2f}")
print(f"Mean max displacement: {mean_max_displacement:.2f}")
print(f"Mean returns to 0: {mean_returns_to_zero:.2f}")
print(f"Expected RMS: {expected_rms:.2f}")