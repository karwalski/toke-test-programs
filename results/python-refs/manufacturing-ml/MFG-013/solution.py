import sys
import csv
import json

def calculate_linear_regression(x_values, y_values):
    n = len(x_values)
    
    # Calculate means
    x_mean = sum(x_values) / n
    y_mean = sum(y_values) / n
    
    # Calculate slope and intercept
    numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
    denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    
    # Calculate r-squared
    y_predicted = [slope * x + intercept for x in x_values]
    ss_res = sum((y_values[i] - y_predicted[i]) ** 2 for i in range(n))
    ss_tot = sum((y_values[i] - y_mean) ** 2 for i in range(n))
    r_squared = 1 - (ss_res / ss_tot)
    
    return slope, intercept, r_squared

# Read CSV from stdin
reader = csv.DictReader(sys.stdin)
reference_values = []
measured_values = []

for row in reader:
    reference_values.append(float(row['reference']))
    measured_values.append(float(row['measured']))

# Calculate regression
slope, intercept, r_squared = calculate_linear_regression(reference_values, measured_values)

# Determine if linear (using r_squared >= 0.95 as threshold)
linear = r_squared >= 0.95

# Create output
result = {
    "slope": round(slope, 2),
    "intercept": round(intercept, 2),
    "r_squared": round(r_squared, 1),
    "linear": linear
}

# Output JSON
print(json.dumps(result, separators=(',', ':')))