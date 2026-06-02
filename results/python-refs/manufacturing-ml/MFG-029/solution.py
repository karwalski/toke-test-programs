import sys
import json

# Read window size
window_size = int(input().strip())

# Read data points
data = []
for line in sys.stdin:
    line = line.strip()
    if line:
        timestamp, value = line.split(',')
        data.append((int(timestamp), float(value)))

# Calculate Simple Moving Average (SMA)
sma = []
for i in range(len(data)):
    if i < window_size - 1:
        sma.append(None)
    else:
        window_sum = sum(data[j][1] for j in range(i - window_size + 1, i + 1))
        avg = window_sum / window_size
        sma.append(round(avg, 2))

# Calculate Weighted Moving Average (WMA)
wma = []
for i in range(len(data)):
    if i < window_size - 1:
        wma.append(None)
    else:
        weighted_sum = 0
        weight_sum = 0
        for j in range(window_size):
            weight = j + 1
            value = data[i - window_size + 1 + j][1]
            weighted_sum += weight * value
            weight_sum += weight
        avg = weighted_sum / weight_sum
        wma.append(round(avg, 2))

# Output JSON
result = {"sma": sma, "wma": wma}
print(json.dumps(result, separators=(',', ':')))