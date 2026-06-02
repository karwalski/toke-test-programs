import sys

# Read input
x_line = input().strip()
y_line = input().strip()

# Parse input
x_values = [float(x) for x in x_line.split(',')]
y_values = [float(y) for y in y_line.split(',')]

n = len(x_values)

# Calculate means
x_mean = sum(x_values) / n
y_mean = sum(y_values) / n

# Calculate slope and intercept
numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))

slope = numerator / denominator
intercept = y_mean - slope * x_mean

# Calculate R-squared
ss_res = sum((y_values[i] - (slope * x_values[i] + intercept)) ** 2 for i in range(n))
ss_tot = sum((y_values[i] - y_mean) ** 2 for i in range(n))
r_squared = 1 - (ss_res / ss_tot)

# Output results
print(f"{slope:.4f}")
print(f"{intercept:.4f}")
print(f"{r_squared:.4f}")