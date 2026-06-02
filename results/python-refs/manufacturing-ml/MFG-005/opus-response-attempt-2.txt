import sys
import csv
import json
import math

csv_reader = csv.DictReader(sys.stdin)
values = []
lsl = None
usl = None

for row in csv_reader:
    values.append(float(row['value']))
    lsl = float(row['lsl'])
    usl = float(row['usl'])

n = len(values)
mean = sum(values) / n
# Sample standard deviation
variance = sum((x - mean) ** 2 for x in values) / (n - 1)
std_dev = math.sqrt(variance)

cpu = (usl - mean) / (3 * std_dev)
cpl = (mean - lsl) / (3 * std_dev)
cpk = min(cpu, cpl)

result = {"cpk": round(cpk, 2)}
print(json.dumps(result, separators=(',', ':')))