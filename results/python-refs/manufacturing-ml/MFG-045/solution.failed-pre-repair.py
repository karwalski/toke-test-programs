import sys
import csv
import json
import statistics

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
values = []
lsl = None
usl = None

for row in reader:
    values.append(float(row['value']))
    lsl = float(row['lsl'])
    usl = float(row['usl'])

# Calculate mean and standard deviation
mean = statistics.mean(values)
stdev = statistics.stdev(values)

# Calculate Pp (Process Performance)
pp = (usl - lsl) / (6 * stdev)

# Calculate Ppk (Process Performance Index)
cpu = (usl - mean) / (3 * stdev)  # Upper capability
cpl = (mean - lsl) / (3 * stdev)  # Lower capability
ppk = min(cpu, cpl)

# Format output as JSON
result = {
    "pp": round(pp, 2),
    "ppk": round(ppk, 2)
}

print(json.dumps(result, separators=(',', ':')))