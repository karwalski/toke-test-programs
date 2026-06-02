import sys
import json

input_line = sys.stdin.read().strip()
raw = input_line.split(',')
values = [float(x) for x in raw]

sorted_values = sorted(values)
n = len(sorted_values)

def percentile(data, p):
    # Linear interpolation, position = p*(n-1)
    pos = p * (n - 1)
    lower = int(pos)
    upper = min(lower + 1, n - 1)
    frac = pos - lower
    return data[lower] + frac * (data[upper] - data[lower])

q1 = percentile(sorted_values, 0.25)
q3 = percentile(sorted_values, 0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = []
for i, value in enumerate(values):
    if value < lower_bound or value > upper_bound:
        v = int(value) if value == int(value) else value
        outliers.append({"index": i, "value": v})

def fmt(x):
    if x == int(x):
        return x
    return x

result = {
    "q1": q1,
    "q3": q3,
    "iqr": iqr,
    "outliers": outliers
}

print(json.dumps(result, separators=(',', ':')))