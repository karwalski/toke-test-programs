import sys
import math

# Read input data
points = []
for line in sys.stdin:
    line = line.strip()
    if line:
        x, y = map(float, line.split())
        points.append((x, y))

n = len(points)
if n == 0:
    exit()

# Calculate sums needed for least squares regression
sum_x = sum(x for x, y in points)
sum_y = sum(y for x, y in points)
sum_xy = sum(x * y for x, y in points)
sum_x2 = sum(x * x for x, y in points)
sum_y2 = sum(y * y for x, y in points)

# Calculate slope (m) and intercept (b)
# m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x^2)
# b = (sum_y - m * sum_x) / n
denominator = n * sum_x2 - sum_x * sum_x
m = (n * sum_xy - sum_x * sum_y) / denominator
b = (sum_y - m * sum_x) / n

# Calculate R-squared
# R^2 = (n * sum_xy - sum_x * sum_y)^2 / ((n * sum_x2 - sum_x^2) * (n * sum_y2 - sum_y^2))
numerator = (n * sum_xy - sum_x * sum_y) ** 2
denominator_r2 = (n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)
r_squared = numerator / denominator_r2

# Calculate RMSE
# RMSE = sqrt(sum((y_actual - y_predicted)^2) / n)
sum_squared_errors = 0
for x, y in points:
    y_predicted = m * x + b
    sum_squared_errors += (y - y_predicted) ** 2
rmse = math.sqrt(sum_squared_errors / n)

# Output results
print(f"y = {m:.4f}x + {b:.4f}")
print(f"R^2: {r_squared:.4f}")
print(f"RMSE: {rmse:.4f}")