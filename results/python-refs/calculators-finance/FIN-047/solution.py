import sys
import math

# Read input
line1 = input().strip()
line2 = input().strip()

# Parse the data
x = [float(num) for num in line1.split(',')]
y = [float(num) for num in line2.split(',')]

n = len(x)

# Calculate means
mean_x = sum(x) / n
mean_y = sum(y) / n

# Calculate numerator and denominators for Pearson correlation
numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))

# Calculate correlation coefficient
denominator = math.sqrt(sum_sq_x * sum_sq_y)

if denominator == 0:
    correlation = 0
else:
    correlation = numerator / denominator

# Output to 4 decimal places
print(f"{correlation:.4f}")