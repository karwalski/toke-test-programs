import sys
import json

lines = []
for line in sys.stdin:
    lines.append(line.strip())

target = float(lines[0].split(',')[1])
deadband = float(lines[1].split(',')[1])
measurements = [float(x) for x in lines[2].split(',')]

current_mean = round(sum(measurements) / len(measurements), 2)
offset = round(current_mean - target, 2)
adjustment_needed = abs(offset) > deadband
adjustment_amount = round(-offset, 2) if adjustment_needed else 0.0

result = {
    "current_mean": current_mean,
    "offset": offset,
    "adjustment_needed": adjustment_needed,
    "adjustment_amount": adjustment_amount
}

print(json.dumps(result, separators=(',', ':')))