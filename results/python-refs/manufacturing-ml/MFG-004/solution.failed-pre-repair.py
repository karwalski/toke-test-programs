import sys
import csv
import json
import math

def calculate_cp(values, lsl, usl):
    # Calculate standard deviation of the values
    n = len(values)
    mean = sum(values) / n
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    std_dev = math.sqrt(variance)
    
    # Calculate Cp = (USL - LSL) / (6 * sigma)
    cp = (usl - lsl) / (6 * std_dev)
    return cp

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
values = []
lsl = None
usl = None

for row in reader:
    values.append(float(row['value']))
    if lsl is None:
        lsl = float(row['lsl'])
    if usl is None:
        usl = float(row['usl'])

# Calculate Cp
cp = calculate_cp(values, lsl, usl)

# Output JSON with cp value rounded to 2 decimal places
output = {"cp": round(cp, 2)}
print(json.dumps(output, separators=(',', ':')))