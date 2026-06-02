import json
import sys
import csv
from io import StringIO

# Read JSON from stdin
input_data = sys.stdin.read().strip()
data = json.loads(input_data)

if not data:
    sys.exit()

# Get all unique keys from all objects to form headers
headers = []
for obj in data:
    for key in obj.keys():
        if key not in headers:
            headers.append(key)

# Use StringIO to capture CSV output
output = StringIO()
writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

# Write header
writer.writerow(headers)

# Write data rows
for obj in data:
    row = [obj.get(key, '') for key in headers]
    writer.writerow(row)

# Print the CSV output
print(output.getvalue().strip())