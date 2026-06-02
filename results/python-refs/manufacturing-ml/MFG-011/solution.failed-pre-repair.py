import sys
import csv
import json
import math

# Read CSV from stdin
csv_reader = csv.DictReader(sys.stdin)
data = list(csv_reader)

# Organize data by operator and part
measurements = {}
for row in data:
    operator = row['operator']
    part = row['part']
    measurement = float(row['measurement'])
    
    if operator not in measurements:
        measurements[operator] = {}
    if part not in measurements[operator]:
        measurements[operator][part] = []
    
    measurements[operator][part].append(measurement)

# Calculate repeatability (within operator variation)
operator_ranges = []
for operator in measurements:
    for part in measurements[operator]:
        part_measurements = measurements[operator][part]
        if len(part_measurements) > 1:
            part_range = max(part_measurements) - min(part_measurements)
            operator_ranges.append(part_range)

# Average range for repeatability
avg_range = sum(operator_ranges) / len(operator_ranges) if operator_ranges else 0
repeatability = avg_range / 1.414  # d2 factor for 2 trials

# Calculate reproducibility (between operator variation)
operator_averages = []
for operator in measurements:
    operator_total = 0
    operator_count = 0
    for part in measurements[operator]:
        for measurement in measurements[operator][part]:
            operator_total += measurement
            operator_count += 1
    operator_avg = operator_total / operator_count if operator_count > 0 else 0
    operator_averages.append(operator_avg)

operator_range = max(operator_averages) - min(operator_averages) if len(operator_averages) > 1 else 0
reproducibility = operator_range / 1.414  # d2 factor for 2 operators

# Calculate total variation (6 sigma)
total_variation = 6 * math.sqrt(repeatability**2 + reproducibility**2)

# Calculate part variation for GRR%
all_measurements = []
for operator in measurements:
    for part in measurements[operator]:
        for measurement in measurements[operator][part]:
            all_measurements.append(measurement)

total_range = max(all_measurements) - min(all_measurements) if all_measurements else 0
part_variation = 6 * (total_range / 5.15)  # Assume normal distribution

# GRR percentage
grr_percent = (total_variation / part_variation) * 100 if part_variation > 0 else 0

# Output JSON
result = {
    "repeatability": round(repeatability, 2),
    "reproducibility": round(reproducibility, 2), 
    "grr_percent": round(grr_percent, 2)
}

print(json.dumps(result, separators=(',', ':')))