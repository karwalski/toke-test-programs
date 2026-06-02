import sys
import json

# Read input
lines = sys.stdin.read().strip().split('\n')
alpha = float(lines[0])
values = list(map(int, lines[1].split(',')))

# Apply single exponential smoothing
smoothed = []
s = values[0]  # Initial smoothed value is the first observation
smoothed.append(float(s))

for i in range(1, len(values)):
    s = alpha * values[i] + (1 - alpha) * s
    smoothed.append(round(s, 2))

# Forecast is the last smoothed value
forecast = smoothed[-1]

# Output as JSON
result = {"smoothed": smoothed, "forecast": forecast}
print(json.dumps(result, separators=(',', ':')))