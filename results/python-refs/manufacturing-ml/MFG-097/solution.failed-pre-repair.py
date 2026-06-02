import csv
import json
import sys

def main():
    # Read CSV from stdin
    reader = csv.DictReader(sys.stdin)
    data = list(reader)
    
    # Convert string values to floats
    for row in data:
        for key in row:
            row[key] = float(row[key])
    
    # Identify parameter columns (non-quality columns)
    # Assume first column is the parameter, rest are quality responses
    param_name = list(data[0].keys())[0]
    quality_cols = [col for col in data[0].keys() if col != param_name]
    
    # Find quality thresholds (use mean as threshold)
    quality_thresholds = {}
    for qual_col in quality_cols:
        values = [row[qual_col] for row in data]
        quality_thresholds[qual_col] = sum(values) / len(values)
    
    # Find rows where all quality criteria are met
    valid_rows = []
    for row in data:
        meets_criteria = True
        for qual_col in quality_cols:
            if row[qual_col] < quality_thresholds[qual_col]:
                meets_criteria = False
                break
        if meets_criteria:
            valid_rows.append(row)
    
    # Find parameter range for valid rows
    if valid_rows:
        param_values = [row[param_name] for row in valid_rows]
        min_param = min(param_values)
        max_param = max(param_values)
        
        # Find best point (highest sum of qualities)
        best_row = max(valid_rows, key=lambda r: sum(r[qual] for qual in quality_cols))
        best_param = best_row[param_name]
    else:
        # Fallback if no clear criteria
        param_values = [row[param_name] for row in data]
        min_param = min(param_values)
        max_param = max(param_values)
        best_row = max(data, key=lambda r: sum(r[qual] for qual in quality_cols))
        best_param = best_row[param_name]
    
    # Calculate robustness (fraction of total range that meets criteria)
    total_param_values = [row[param_name] for row in data]
    total_range = max(total_param_values) - min(total_param_values)
    valid_range = max_param - min_param
    robustness = round(valid_range / total_range, 2) if total_range > 0 else 0.0
    
    # Create output
    result = {
        "optimal_window": {
            param_name: {
                "min": int(min_param),
                "max": int(max_param)
            }
        },
        "best_point": {
            param_name: int(best_param)
        },
        "robustness": robustness
    }
    
    print(json.dumps(result, separators=(',', ':')))

if __name__ == "__main__":
    main()