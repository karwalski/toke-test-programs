import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
batches = []
total_units = 0
total_passed = 0

for row in reader:
    batch_id = row['batch_id']
    total = int(row['total'])
    passed = int(row['passed'])
    
    fpy = passed / total
    batches.append({"batch_id": batch_id, "fpy": fpy})
    
    total_units += total
    total_passed += passed

overall_fpy = total_passed / total_units

result = {
    "overall_fpy": overall_fpy,
    "per_batch": batches
}

print(json.dumps(result, separators=(',', ':')))