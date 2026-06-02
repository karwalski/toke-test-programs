import sys
import json

# Read CSV data from stdin
lines = sys.stdin.read().strip().split('\n')
header = lines[0]
data_lines = lines[1:]

# Parse the data
x_values = []
y_values = []

for line in data_lines:
    x, y = line.split(',')
    x_values.append(float(x))
    y_values.append(float(y))

n = len(x_values)

# Calculate means
x_mean = sum(x_values) / n
y_mean = sum(y_values) / n

# Calculate slope (beta1) and intercept (beta0)
numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))

slope = numerator / denominator
intercept = y_mean - slope * x_mean

# Calculate R-squared
y_pred = [slope * x + intercept for x in x_values]
ss_res = sum((y_values[i] - y_pred[i]) ** 2 for i in range(n))
ss_tot = sum((y_values[i] - y_mean) ** 2 for i in range(n))
r_squared = 1 - (ss_res / ss_tot)

# Output JSON
result = {
    "slope": slope,
    "intercept": intercept,
    "r_squared": r_squared
}

print(json.dumps(result, separators=(',', ':')))