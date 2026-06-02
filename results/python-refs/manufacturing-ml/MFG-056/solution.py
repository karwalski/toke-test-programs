import sys
import json
import csv

# Read CSV data from stdin
reader = csv.reader(sys.stdin)
headers = next(reader)
rows = []
for row in reader:
    rows.append([float(val) for val in row])

# Calculate min and max for each column
num_cols = len(headers)
mins = [float('inf')] * num_cols
maxs = [float('-inf')] * num_cols

for row in rows:
    for i in range(num_cols):
        mins[i] = min(mins[i], row[i])
        maxs[i] = max(maxs[i], row[i])

# Normalize data to 0-1 range
normalized = []
for row in rows:
    norm_row = []
    for i in range(num_cols):
        if maxs[i] == mins[i]:
            norm_val = 0.0
        else:
            norm_val = (row[i] - mins[i]) / (maxs[i] - mins[i])
        norm_row.append(norm_val)
    normalized.append(norm_row)

# Convert to integers where they are whole numbers for exact output match
mins = [int(x) if x == int(x) else x for x in mins]
maxs = [int(x) if x == int(x) else x for x in maxs]

# Create output JSON
result = {
    "normalised": normalized,
    "min": mins,
    "max": maxs
}

print(json.dumps(result, separators=(',', ':')))