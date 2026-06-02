mr_bar = 0.2, ucl = 0.65. 0.65/0.2 = 3.25... Let me check: with rounded mr_bar=0.2, D4=3.267 gives 0.6534 → 0.65. 

import sys
import json

input_data = sys.stdin.read().strip()
measurements = [float(x) for x in input_data.split(',')]

moving_ranges = []
for i in range(1, len(measurements)):
    mr = abs(measurements[i] - measurements[i-1])
    moving_ranges.append(mr)

mr_bar = sum(moving_ranges) / len(moving_ranges)
mr_bar = round(mr_bar, 2)

D4 = 3.267
D3 = 0

ucl = round(D4 * mr_bar, 2)
lcl = round(D3 * mr_bar, 2)

result = {"mr_bar": mr_bar, "ucl": ucl, "lcl": lcl}
print(json.dumps(result, separators=(',', ':')))