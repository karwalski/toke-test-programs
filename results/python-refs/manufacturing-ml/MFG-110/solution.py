import csv
import json
import sys

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
fmea_items = []

for row in reader:
    failure_mode = row['failure_mode']
    severity = int(row['severity'])
    occurrence = int(row['occurrence'])
    detection = int(row['detection'])
    
    rpn = severity * occurrence * detection
    
    fmea_items.append({
        'failure_mode': failure_mode,
        'rpn': rpn
    })

# Sort by RPN descending
fmea_items.sort(key=lambda x: x['rpn'], reverse=True)

# Output JSON
result = {'fmea': fmea_items}
print(json.dumps(result, separators=(',', ':')))