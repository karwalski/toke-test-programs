import json
import csv
import sys

# Read JSON from stdin
json_data = sys.stdin.read().strip()
data = json.loads(json_data)

# Get headers from first object
if data:
    headers = list(data[0].keys())
    
    # Create CSV writer
    writer = csv.writer(sys.stdout)
    
    # Write header row
    writer.writerow(headers)
    
    # Write data rows
    for obj in data:
        row = [obj[key] for key in headers]
        writer.writerow(row)