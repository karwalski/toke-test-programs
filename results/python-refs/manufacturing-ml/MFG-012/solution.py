import csv
import json
import sys
from statistics import mean

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
reference_values = []
measured_values = []

for row in reader:
    reference_values.append(float(row['reference']))
    measured_values.append(float(row['measured']))

# Calculate bias
bias = mean(measured_values) - mean(reference_values)

# Calculate bias percentage
bias_percent = (bias / mean(reference_values)) * 100

# Determine if bias is significant (using a simple threshold of 0.5%)
significant = abs(bias_percent) > 0.5

# Output JSON
result = {
    "bias": round(bias, 2),
    "bias_percent": round(bias_percent, 1),
    "significant": significant
}

print(json.dumps(result, separators=(',', ':')))