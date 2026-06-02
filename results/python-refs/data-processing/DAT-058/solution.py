import sys
import csv
import math

def mean(values):
    return sum(values) / len(values)

def pearson_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0
    
    mean_x = mean(x)
    mean_y = mean(y)
    
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    
    sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    if denominator == 0:
        return 0
    
    return numerator / denominator

# Read CSV from stdin
reader = csv.reader(sys.stdin)
rows = list(reader)

# Get headers and data
headers = rows[0]
data_rows = rows[1:]

# Convert data to numeric columns
columns = {}
for i, header in enumerate(headers):
    columns[header] = [float(row[i]) for row in data_rows]

# Compute correlation matrix
correlation_matrix = {}
for col1 in headers:
    correlation_matrix[col1] = {}
    for col2 in headers:
        corr = pearson_correlation(columns[col1], columns[col2])
        correlation_matrix[col1][col2] = corr

# Output correlation matrix as CSV
print(',' + ','.join(headers))
for col1 in headers:
    row = [col1]
    for col2 in headers:
        row.append(f"{correlation_matrix[col1][col2]:.4f}")
    print(','.join(row))