import csv
import json
import sys
import math

def calculate_pearson_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0
    
    # Calculate means
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Calculate numerator and denominators
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    # Handle perfect correlation case
    if sum_sq_x == 0 or sum_sq_y == 0:
        return 1.0 if all(a == b for a, b in zip(x, y)) else 0.0
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    return numerator / denominator

# Read CSV from stdin
input_data = sys.stdin.read().strip()
lines = input_data.split('\n')
reader = csv.reader(lines)

# Get headers and data
headers = next(reader)
data = []
for row in reader:
    data.append([float(val) for val in row])

# Transpose data to get columns
columns = list(zip(*data))
num_sensors = len(columns)

# Calculate correlation matrix
correlation_matrix = []
for i in range(num_sensors):
    row = []
    for j in range(num_sensors):
        if i == j:
            correlation = 1.0
        else:
            correlation = calculate_pearson_correlation(list(columns[i]), list(columns[j]))
        row.append(correlation)
    correlation_matrix.append(row)

# Output as JSON
result = {"correlation_matrix": correlation_matrix}
print(json.dumps(result, separators=(',', ':')))