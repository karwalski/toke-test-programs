import sys
import json

# Read input from stdin
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse the input
target = float(lines[0].split(',')[1])
deadband = float(lines[1].split(',')[1])
measurements = [float(x) for x in lines[2].split(',')]

# Calculate current mean
current_mean = sum(measurements) / len(measurements)

# Calculate offset from target
offset = current_mean - target

# Check if adjustment is needed (offset exceeds deadband)
adjustment_needed = abs(offset) > deadband

# Calculate adjustment amount (negative of offset to re-center)
adjustment_amount = -offset if adjustment_needed else 0.0

# Create output dictionary
result = {
    "current_mean": current_mean,
    "offset": offset,
    "adjustment_needed": adjustment_needed,
    "adjustment_amount": adjustment_amount
}

# Output JSON without spaces after separators
print(json.dumps(result, separators=(',', ':')))