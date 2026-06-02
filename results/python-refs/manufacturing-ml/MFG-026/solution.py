import sys
import json
import math

input_line = sys.stdin.read().strip()
measurements = [float(x) for x in input_line.split(',')]

n = len(measurements)
mean = sum(measurements) / n

variance = sum((x - mean) ** 2 for x in measurements) / n
std_dev = math.sqrt(variance)

anomalies = []
for i, value in enumerate(measurements):
    if std_dev != 0:
        z_score = (value - mean) / std_dev
        if abs(z_score) > 2.5:
            anomalies.append({
                "index": i,
                "value": value,
                "z_score": round(z_score, 2)
            })

result = {"anomalies": anomalies}
print(json.dumps(result, separators=(',', ':')))