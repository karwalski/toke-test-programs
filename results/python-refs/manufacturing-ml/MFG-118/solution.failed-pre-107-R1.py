import sys
import csv
import json
import math

def calculate_correlation(x, y):
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
    
    # Handle division by zero
    denominator = math.sqrt(sum_sq_x * sum_sq_y)
    if denominator == 0:
        return 0
    
    return numerator / denominator

# Read CSV from stdin
lines = []
for line in sys.stdin:
    lines.append(line.strip())

# Parse CSV
reader = csv.DictReader(lines)
data = list(reader)

# Extract defect_rate column
defect_rates = [float(row['defect_rate']) for row in data]

# Calculate correlations for each process variable
correlations = []
process_variables = [col for col in data[0].keys() if col != 'defect_rate']

for var in process_variables:
    values = [float(row[var]) for row in data]
    correlation = calculate_correlation(values, defect_rates)
    correlations.append({
        'variable': var,
        'r': round(correlation, 2)
    })

# Sort by absolute correlation value (descending)
correlations.sort(key=lambda x: abs(x['r']), reverse=True)

# Find likely root cause (highest absolute correlation)
likely_root_cause = correlations[0]['variable'] if correlations else ""

# Output JSON
result = {
    "correlations": correlations,
    "likely_root_cause": likely_root_cause
}

print(json.dumps(result, separators=(',', ':')))