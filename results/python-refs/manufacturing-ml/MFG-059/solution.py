import csv
import json
import sys
import math

def calculate_correlation(x, y):
    n = len(x)
    if n == 0:
        return 0.0
    
    # Calculate means
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    
    # Calculate correlation coefficient
    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    sum_sq_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    sum_sq_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    
    if denominator == 0:
        return 0.0
    
    correlation = numerator / denominator
    return correlation

# Read CSV from stdin
reader = csv.reader(sys.stdin)
headers = next(reader)
rows = list(reader)

# Extract feature columns and target column
feature_names = headers[:-1]
target_name = headers[-1]

# Convert data to numeric
features = []
target = []

for row in rows:
    target.append(float(row[-1]))
    feature_row = []
    for i in range(len(row) - 1):
        feature_row.append(float(row[i]))
    features.append(feature_row)

# Calculate correlations
correlations = []
for i, feature_name in enumerate(feature_names):
    feature_values = [row[i] for row in features]
    corr = calculate_correlation(feature_values, target)
    correlations.append((feature_name, corr))

# Sort by correlation (descending)
correlations.sort(key=lambda x: x[1], reverse=True)

# Format output
rankings = []
for feature_name, corr in correlations:
    rankings.append({"feature": feature_name, "correlation": corr})

output = {"rankings": rankings}
print(json.dumps(output, separators=(',', ':')))