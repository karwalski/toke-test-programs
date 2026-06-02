import sys
import csv
import json
import statistics

# Read CSV data from stdin
csv_reader = csv.DictReader(sys.stdin)
shift_data = {}

for row in csv_reader:
    shift = row['shift']
    measurement = float(row['measurement'])
    
    if shift not in shift_data:
        shift_data[shift] = []
    shift_data[shift].append(measurement)

# Calculate metrics for each shift
shifts = []
best_shift = None
best_mean = None

for shift, measurements in shift_data.items():
    mean = statistics.mean(measurements)
    std = statistics.stdev(measurements) if len(measurements) > 1 else 0.0
    n = len(measurements)
    
    shifts.append({
        "shift": shift,
        "mean": round(mean, 2),
        "std": round(std, 2),
        "n": n
    })
    
    # Track best shift (lowest mean)
    if best_shift is None or mean < best_mean:
        best_shift = shift
        best_mean = mean

# Sort shifts by name for consistent output
shifts.sort(key=lambda x: x['shift'])

# Create output
result = {
    "shifts": shifts,
    "best_shift": best_shift
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))