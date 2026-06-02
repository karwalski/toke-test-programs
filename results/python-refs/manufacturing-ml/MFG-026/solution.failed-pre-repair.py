import sys
import json
import math

# Read CSV input from stdin
input_line = sys.stdin.read().strip()
measurements = [float(x) for x in input_line.split(',')]

# Calculate mean
mean = sum(measurements) / len(measurements)

# Calculate standard deviation
variance = sum((x - mean) ** 2 for x in measurements) / len(measurements)
std_dev = math.sqrt(variance)

# Find anomalies (|z-score| > 2)
anomalies = []
for i, value in enumerate(measurements):
    if std_dev != 0:  # Avoid division by zero
        z_score = (value - mean) / std_dev
        if abs(z_score) > 2:
            anomalies.append({
                "index": i,
                "value": value,
                "z_score": round(z_score, 2)
            })

# Output JSON
result = {"anomalies": anomalies}
print(json.dumps(result, separators=(',', ':')))