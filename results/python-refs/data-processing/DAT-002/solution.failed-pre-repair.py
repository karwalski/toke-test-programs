import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
data = []

for row in reader:
    data.append(dict(row))

# Output JSON with exact formatting
print(json.dumps(data, indent=2))