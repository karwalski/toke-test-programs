import csv
import sys
import json
import math

# Read CSV data from stdin
reader = csv.DictReader(sys.stdin)
phase1_values = []
phase2_values = []

for row in reader:
    phase = int(row['phase'])
    value = float(row['value'])
    
    if phase == 1:
        phase1_values.append(value)
    elif phase == 2:
        phase2_values.append(value)

# Calculate mean and standard deviation for each phase
def calculate_stats(values):
    n = len(values)
    mean = sum(values) / n
    
    # Calculate standard deviation
    variance = sum((x - mean) ** 2 for x in values) / n
    std = math.sqrt(variance)
    
    return mean, std

phase1_mean, phase1_std = calculate_stats(phase1_values)
phase2_mean, phase2_std = calculate_stats(phase2_values)

# Calculate improvement metrics
mean_shift = phase2_mean - phase1_mean
variability_reduction = (phase1_std - phase2_std) / phase1_std

# Create output JSON
result = {
    "phase1": {
        "mean": round(phase1_mean, 2),
        "std": round(phase1_std, 2)
    },
    "phase2": {
        "mean": round(phase2_mean, 2),
        "std": round(phase2_std, 2)
    },
    "improvement": {
        "mean_shift": round(mean_shift, 2),
        "variability_reduction": round(variability_reduction, 2)
    }
}

print(json.dumps(result, separators=(',', ':')))