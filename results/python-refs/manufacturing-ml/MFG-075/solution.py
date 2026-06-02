import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)

# Initialize category totals
totals = {
    'prevention': 0,
    'appraisal': 0,
    'internal_failure': 0,
    'external_failure': 0
}

# Process each row
for row in reader:
    category = row['category']
    cost = int(row['cost'])
    totals[category] += cost

# Calculate total cost of quality
total_coq = sum(totals.values())

# Calculate failure ratio
failure_costs = totals['internal_failure'] + totals['external_failure']
failure_ratio = round(failure_costs / total_coq, 2)

# Create output dictionary
output = {
    'prevention': totals['prevention'],
    'appraisal': totals['appraisal'],
    'internal_failure': totals['internal_failure'],
    'external_failure': totals['external_failure'],
    'total_coq': total_coq,
    'failure_ratio': failure_ratio
}

# Output JSON
print(json.dumps(output, separators=(',', ':')))