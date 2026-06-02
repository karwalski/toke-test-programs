import sys
import json
import math

# Read input from stdin
input_data = sys.stdin.read().strip()
defect_counts = list(map(int, input_data.split(',')))

# Calculate c-bar (average defect count)
c_bar = sum(defect_counts) / len(defect_counts)

# Calculate control limits
# UCL = c_bar + 3 * sqrt(c_bar)
# LCL = c_bar - 3 * sqrt(c_bar), but not less than 0
ucl = c_bar + 3 * math.sqrt(c_bar)
lcl = max(0.0, c_bar - 3 * math.sqrt(c_bar))

# Find out of control points (indices where count > UCL or count < LCL)
out_of_control = []
for i, count in enumerate(defect_counts):
    if count > ucl or count < lcl:
        out_of_control.append(i)

# Create output dictionary
result = {
    "c_bar": round(c_bar, 2),
    "ucl": round(ucl, 2),
    "lcl": round(lcl, 2),
    "out_of_control": out_of_control
}

# Output as JSON
print(json.dumps(result, separators=(',', ':')))