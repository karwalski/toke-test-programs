import sys
import csv
import json
import math

# Read CSV from stdin
csv_reader = csv.DictReader(sys.stdin)
values = []
lsl = None
usl = None

for row in csv_reader:
    values.append(float(row['value']))
    lsl = float(row['lsl'])
    usl = float(row['usl'])

# Calculate process statistics
n = len(values)
mean = sum(values) / n
variance = sum((x - mean) ** 2 for x in values) / (n - 1)
std_dev = math.sqrt(variance)

# Calculate Cpk
cpu = (usl - mean) / (3 * std_dev)
cpl = (mean - lsl) / (3 * std_dev)
cpk = min(cpu, cpl)

# Output as JSON
result = {"cpk": round(cpk, 2)}
print(json.dumps(result))