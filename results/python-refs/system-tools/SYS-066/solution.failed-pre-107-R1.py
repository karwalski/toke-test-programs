import csv
import json
import sys

# Read CSV from stdin
csv_reader = csv.DictReader(sys.stdin)
result = []

for row in csv_reader:
    result.append(row)

# Output JSON array with specific formatting to match expected output
print(json.dumps(result, separators=(',', ':')))