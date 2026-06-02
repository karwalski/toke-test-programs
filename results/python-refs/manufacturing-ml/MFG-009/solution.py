import sys
import json

# Read input from stdin
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse input
target = float(lines[0].split(',')[1])
slack = float(lines[1].split(',')[1])
measurements = [float(x) for x in lines[2].split(',')]

# Calculate CUSUM values
cusum_pos = []
cusum_neg = []
signal = False

pos_sum = 0.0
neg_sum = 0.0

for measurement in measurements:
    # Calculate positive CUSUM
    pos_sum = max(0.0, pos_sum + (measurement - target) - slack)
    cusum_pos.append(pos_sum)
    
    # Calculate negative CUSUM
    neg_sum = max(0.0, neg_sum + (target - measurement) - slack)
    cusum_neg.append(neg_sum)

# Check for signal (if any CUSUM value is greater than 0)
for val in cusum_pos + cusum_neg:
    if val > 0:
        signal = True
        break

# Output JSON
result = {
    "cusum_pos": cusum_pos,
    "cusum_neg": cusum_neg,
    "signal": signal
}

print(json.dumps(result, separators=(',', ':')))