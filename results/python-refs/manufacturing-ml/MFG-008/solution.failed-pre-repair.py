import sys
import json

# Read input from stdin
input_data = sys.stdin.read().strip()
measurements = [float(x) for x in input_data.split(',')]

# Calculate moving ranges
moving_ranges = []
for i in range(1, len(measurements)):
    mr = abs(measurements[i] - measurements[i-1])
    moving_ranges.append(mr)

# Calculate MR-bar (average of moving ranges)
mr_bar = sum(moving_ranges) / len(moving_ranges)

# Calculate UCL and LCL for moving range chart
# For moving range chart: UCL = D4 * MR-bar, LCL = D3 * MR-bar
# For n=2 (consecutive measurements): D4 = 3.267, D3 = 0
D4 = 3.267
D3 = 0

ucl = D4 * mr_bar
lcl = D3 * mr_bar

# Round to appropriate decimal places to match expected output
mr_bar = round(mr_bar, 1)
ucl = round(ucl, 2)
lcl = round(lcl, 1)

# Output as JSON
result = {"mr_bar": mr_bar, "ucl": ucl, "lcl": lcl}
print(json.dumps(result, separators=(',', ':')))