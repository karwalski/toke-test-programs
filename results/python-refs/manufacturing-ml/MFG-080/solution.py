import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
errors = []
calibration_status = "pass"
adjustment_needed = False

for row in reader:
    reference = float(row['reference'])
    reading = float(row['reading'])
    tolerance = float(row['tolerance'])
    
    error = abs(reading - reference)
    errors.append(error)
    
    # Check if this reading exceeds tolerance
    if error > tolerance:
        calibration_status = "fail"
        adjustment_needed = True

# Calculate results
max_error = max(errors) if errors else 0.0

# Output JSON
result = {
    "calibration_status": calibration_status,
    "max_error": max_error,
    "adjustment_needed": adjustment_needed
}

print(json.dumps(result, separators=(',', ':')))