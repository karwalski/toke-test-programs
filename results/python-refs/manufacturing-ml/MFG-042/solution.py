import sys
import json

# Read input
lines = sys.stdin.read().strip().split('\n')
num_bins = int(lines[0])
measurements = list(map(float, lines[1].split(',')))

# Calculate bin boundaries
min_val = min(measurements)
max_val = max(measurements)
bin_width = (max_val - min_val) / num_bins

# Create bins
bins = []
for i in range(num_bins):
    lower = min_val + i * bin_width
    upper = min_val + (i + 1) * bin_width
    count = 0
    
    # Count measurements in this bin
    for measurement in measurements:
        if i == num_bins - 1:  # Last bin includes upper boundary
            if lower <= measurement <= upper:
                count += 1
        else:  # Other bins exclude upper boundary
            if lower <= measurement < upper:
                count += 1
    
    bins.append({
        "lower": round(lower, 2),
        "upper": round(upper, 2),
        "count": count
    })

# Output JSON
result = {"bins": bins}
print(json.dumps(result, separators=(',', ':')))