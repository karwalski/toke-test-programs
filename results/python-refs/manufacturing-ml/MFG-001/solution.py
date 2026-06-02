import sys
import json

# Read input from stdin
input_line = sys.stdin.read().strip()

# Parse CSV values
measurements = [float(x) for x in input_line.split(',')]

# Calculate mean
mean_value = sum(measurements) / len(measurements)

# Output JSON
result = {"mean": mean_value}
print(json.dumps(result, separators=(',', ':')))