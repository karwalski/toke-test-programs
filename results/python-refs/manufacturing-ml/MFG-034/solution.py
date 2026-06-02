import sys
import csv
import json
from io import StringIO

# Read all input from stdin
input_data = sys.stdin.read().strip()

# Parse the input
lines = input_data.split('\n')
failure_threshold = float(lines[0].split(',')[1])

# Parse CSV data
csv_data = '\n'.join(lines[1:])
reader = csv.DictReader(StringIO(csv_data))

times = []
degradations = []

for row in reader:
    times.append(float(row['time']))
    degradations.append(float(row['degradation']))

# Calculate linear regression slope using least squares
n = len(times)
sum_x = sum(times)
sum_y = sum(degradations)
sum_xy = sum(t * d for t, d in zip(times, degradations))
sum_x2 = sum(t * t for t in times)

# Calculate slope (m) and intercept (b) for y = mx + b
slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
intercept = (sum_y - slope * sum_x) / n

# Current degradation is the last value
current_degradation = degradations[-1]

# Calculate time to failure
# failure_threshold = slope * t + intercept
# t = (failure_threshold - intercept) / slope
time_to_failure = (failure_threshold - intercept) / slope

# Current time is the last time value
current_time = times[-1]

# Estimated time to failure from current time
estimated_ttf = time_to_failure - current_time

# Prepare output
result = {
    "estimated_ttf": estimated_ttf,
    "slope": slope,
    "current_degradation": current_degradation
}

print(json.dumps(result, separators=(',', ':')))