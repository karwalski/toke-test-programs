import sys
import csv
import json
from io import StringIO

# Read input from stdin
input_data = sys.stdin.read().strip()

# Parse CSV data
csv_reader = csv.DictReader(StringIO(input_data))
data = list(csv_reader)

# Extract parameter names (all columns except 'quality')
param_names = [col for col in csv_reader.fieldnames if col != 'quality']

# Convert data to appropriate types
for row in data:
    for param in param_names:
        row[param] = int(row[param])
    row['quality'] = int(row['quality'])

# Find unique values for each parameter
param_ranges = {}
for param in param_names:
    param_ranges[param] = sorted(set(int(row[param]) for row in data))

# Grid search to find optimal parameters
best_quality = -1
best_params = {}

# Generate all combinations of parameters
def generate_combinations(param_ranges, param_names, current_params, index):
    global best_quality, best_params
    
    if index == len(param_names):
        # Calculate predicted quality for this parameter combination
        # Use the maximum quality from historical data with these exact parameters
        quality = get_quality_for_params(current_params)
        if quality > best_quality:
            best_quality = quality
            best_params = current_params.copy()
        return
    
    param_name = param_names[index]
    for value in param_ranges[param_name]:
        current_params[param_name] = value
        generate_combinations(param_ranges, param_names, current_params, index + 1)

def get_quality_for_params(params):
    # Find exact matches in historical data
    for row in data:
        match = True
        for param, value in params.items():
            if row[param] != value:
                match = False
                break
        if match:
            return row['quality']
    return 0

# Start grid search
generate_combinations(param_ranges, param_names, {}, 0)

# Output result
result = {
    "optimal_params": best_params,
    "predicted_quality": best_quality
}

print(json.dumps(result, separators=(',', ':')))