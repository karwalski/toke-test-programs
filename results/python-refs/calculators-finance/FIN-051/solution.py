import sys

# Read input from stdin
input_line = input().strip()

# Parse the comma-separated numbers
numbers = [float(x) for x in input_line.split(',')]

# Calculate mean
mean = sum(numbers) / len(numbers)

# Calculate standard deviation
variance = sum((x - mean) ** 2 for x in numbers) / len(numbers)
std_dev = variance ** 0.5

# Calculate z-scores
z_scores = [(x - mean) / std_dev for x in numbers]

# Format to 4 decimal places and join with commas
output = ','.join(f'{z:.4f}' for z in z_scores)

print(output)