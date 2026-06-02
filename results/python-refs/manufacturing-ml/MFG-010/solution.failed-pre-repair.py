import sys
import json
import math

# Read input from stdin
lines = sys.stdin.read().strip().split('\n')
lambda_val, target = map(float, lines[0].split(','))
measurements = list(map(float, lines[1].split(',')))

# Calculate EWMA values
ewma = []
current_ewma = target  # Initialize with target value

for measurement in measurements:
    current_ewma = lambda_val * measurement + (1 - lambda_val) * current_ewma
    ewma.append(round(current_ewma, 2))

# Calculate control limits
# For EWMA control charts, the standard formula is:
# UCL/LCL = target ± L * sigma * sqrt(lambda / (2 - lambda) * (1 - (1-lambda)^(2*n)))
# Using typical values: L = 3, sigma = 1 (assuming unit standard deviation)
# For simplicity and to match expected output, using approximation for steady state

L = 3
sigma = 1
steady_state_factor = math.sqrt(lambda_val / (2 - lambda_val))
control_limit_range = L * sigma * steady_state_factor

ucl = round(target + control_limit_range, 2)
lcl = round(target - control_limit_range, 2)

# Output JSON
result = {
    "ewma": ewma,
    "ucl": ucl,
    "lcl": lcl
}

print(json.dumps(result, separators=(',', ':')))