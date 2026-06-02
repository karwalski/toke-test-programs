import sys
import json
import math

# Read input from stdin
input_line = sys.stdin.read().strip()

# Parse CSV values
measurements = [float(x) for x in input_line.split(',')]

# Calculate sample standard deviation
n = len(measurements)
mean = sum(measurements) / n

# Calculate sum of squared differences
sum_sq_diff = sum((x - mean) ** 2 for x in measurements)

# Sample standard deviation (divide by n-1)
std_dev = math.sqrt(sum_sq_diff / (n - 1))

# Round to 2 decimal places and output as JSON
result = {"std_dev": round(std_dev, 2)}
print(json.dumps(result, separators=(',', ':')))