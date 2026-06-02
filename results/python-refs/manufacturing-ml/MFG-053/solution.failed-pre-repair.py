import sys
import csv
import json

# Read CSV from stdin
csv_reader = csv.DictReader(sys.stdin)
sensors = list(csv_reader)

# Calculate weighted average
total_weighted_value = 0
total_weight = 0

for sensor in sensors:
    value = float(sensor['value'])
    weight = float(sensor['weight'])
    total_weighted_value += value * weight
    total_weight += weight

fused_value = total_weighted_value / total_weight

# Calculate confidence as average of weights
confidence = total_weight / len(sensors)

# Round to 2 decimal places
fused_value = round(fused_value, 2)
confidence = round(confidence, 2)

# Output JSON
result = {"fused_value": fused_value, "confidence": confidence}
print(json.dumps(result, separators=(',', ':')))