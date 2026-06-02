import sys
import json
import csv
from collections import defaultdict

# Read CSV from stdin
input_data = sys.stdin.read().strip()
lines = input_data.split('\n')

# Parse CSV
reader = csv.DictReader(lines)
data = defaultdict(list)

for row in reader:
    reference = float(row['reference'])
    measurement = float(row['measurement'])
    data[reference].append(measurement)

# Calculate bias at each reference point
biases = []
bias_values = []

for reference in sorted(data.keys()):
    measurements = data[reference]
    avg_measurement = sum(measurements) / len(measurements)
    bias = avg_measurement - reference
    biases.append({"reference": int(reference), "bias": bias})
    bias_values.append(bias)

# Calculate linearity percentage
measurement_range = max(data.keys()) - min(data.keys())
bias_range = max(bias_values) - min(bias_values)
linearity_percent = (bias_range / (2 * measurement_range)) * 100

# Determine acceptability (assuming < 10% is acceptable)
acceptable = linearity_percent < 10

# Create output
output = {
    "biases": biases,
    "linearity_percent": linearity_percent,
    "acceptable": acceptable
}

print(json.dumps(output, separators=(',', ':')))