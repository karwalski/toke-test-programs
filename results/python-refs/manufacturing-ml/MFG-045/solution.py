import sys
import csv
import json
import math

reader = csv.DictReader(sys.stdin)
values = []
lsl = None
usl = None

for row in reader:
    values.append(float(row['value']))
    lsl = float(row['lsl'])
    usl = float(row['usl'])

n = len(values)
mean = sum(values) / n
variance = sum((x - mean) ** 2 for x in values) / n
stdev = math.sqrt(variance)

pp = (usl - lsl) / (6 * stdev)
cpu = (usl - mean) / (3 * stdev)
cpl = (mean - lsl) / (3 * stdev)
ppk = min(cpu, cpl)

result = {
    "pp": round(pp, 2),
    "ppk": round(ppk, 2)
}

print(json.dumps(result, separators=(',', ':')))