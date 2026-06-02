import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
rows = list(reader)

# Calculate total percentage and check validity
total_percent = 0.0
out_of_spec = []

for row in rows:
    element = row['element']
    min_val = float(row['min'])
    max_val = float(row['max'])
    actual_val = float(row['actual'])
    
    total_percent += actual_val
    
    # Check if actual value is within spec
    if actual_val < min_val or actual_val > max_val:
        out_of_spec.append(element)

# Check if total is valid (assuming 100% is the target)
valid = total_percent == 100.0 and len(out_of_spec) == 0

# Output JSON
result = {
    "total_percent": total_percent,
    "valid": valid,
    "out_of_spec": out_of_spec
}

print(json.dumps(result, separators=(',', ':')))