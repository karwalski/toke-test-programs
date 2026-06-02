import sys
import csv
import json

# Read all input
lines = sys.stdin.read().strip().split('\n')

# Parse threshold from first line
threshold_line = lines[0]
threshold = float(threshold_line.split(',')[1])

# Parse CSV data starting from line 1 (header) and line 2+ (data)
reader = csv.DictReader(lines[1:])
data = list(reader)

# Calculate rates of change
rates = []
alerts = []

for i in range(1, len(data)):
    prev_value = float(data[i-1]['value'])
    curr_value = float(data[i]['value'])
    rate = curr_value - prev_value
    rates.append(rate)
    
    # Check for alerts (rapid changes)
    if rate > threshold:
        alerts.append({"index": i, "rate": rate})

# Create output
result = {
    "rates": rates,
    "alerts": alerts
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))