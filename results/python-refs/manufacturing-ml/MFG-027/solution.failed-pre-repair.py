import sys
import json

# Read input from stdin
input_line = sys.stdin.read().strip()
values = [float(x) for x in input_line.split(',')]

# Sort values for quartile calculation
sorted_values = sorted(values)
n = len(sorted_values)

# Calculate Q1 (25th percentile)
q1_pos = 0.25 * (n + 1)
if q1_pos == int(q1_pos):
    q1 = sorted_values[int(q1_pos) - 1]
else:
    lower = int(q1_pos) - 1
    upper = int(q1_pos)
    fraction = q1_pos - int(q1_pos)
    q1 = sorted_values[lower] + fraction * (sorted_values[upper] - sorted_values[lower])

# Calculate Q3 (75th percentile)
q3_pos = 0.75 * (n + 1)
if q3_pos == int(q3_pos):
    q3 = sorted_values[int(q3_pos) - 1]
else:
    lower = int(q3_pos) - 1
    upper = int(q3_pos)
    fraction = q3_pos - int(q3_pos)
    q3 = sorted_values[lower] + fraction * (sorted_values[upper] - sorted_values[lower])

# Calculate IQR
iqr = q3 - q1

# Calculate outlier bounds
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Find outliers
outliers = []
for i, value in enumerate(values):
    if value < lower_bound or value > upper_bound:
        outliers.append({"index": i, "value": value})

# Create output
result = {
    "q1": q1,
    "q3": q3,
    "iqr": iqr,
    "outliers": outliers
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))