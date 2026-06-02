import sys
import csv
import json
import math

def read_input():
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    # Parse method from first line
    method_line = lines[0]
    method = method_line.split(',')[1]
    
    # Parse CSV data
    csv_lines = lines[1:]
    reader = csv.DictReader(csv_lines)
    
    values = []
    for row in reader:
        val = row['value']
        if val == 'NaN':
            values.append(None)
        else:
            values.append(float(val))
    
    return method, values

def impute_mean(values):
    # Calculate mean of non-missing values
    non_missing = [v for v in values if v is not None]
    if not non_missing:
        return values, 0
    
    mean_val = sum(non_missing) / len(non_missing)
    
    imputed_count = 0
    result = []
    for val in values:
        if val is None:
            result.append(mean_val)
            imputed_count += 1
        else:
            result.append(val)
    
    return result, imputed_count

def impute_median(values):
    # Calculate median of non-missing values
    non_missing = [v for v in values if v is not None]
    if not non_missing:
        return values, 0
    
    non_missing.sort()
    n = len(non_missing)
    if n % 2 == 0:
        median_val = (non_missing[n//2 - 1] + non_missing[n//2]) / 2
    else:
        median_val = non_missing[n//2]
    
    imputed_count = 0
    result = []
    for val in values:
        if val is None:
            result.append(median_val)
            imputed_count += 1
        else:
            result.append(val)
    
    return result, imputed_count

def impute_linear(values):
    result = values[:]
    imputed_count = 0
    
    for i in range(len(values)):
        if values[i] is None:
            # Find previous non-missing value
            prev_idx = None
            prev_val = None
            for j in range(i-1, -1, -1):
                if values[j] is not None:
                    prev_idx = j
                    prev_val = values[j]
                    break
            
            # Find next non-missing value
            next_idx = None
            next_val = None
            for j in range(i+1, len(values)):
                if values[j] is not None:
                    next_idx = j
                    next_val = values[j]
                    break
            
            # Interpolate
            if prev_idx is not None and next_idx is not None:
                # Linear interpolation
                x0, y0 = prev_idx, prev_val
                x1, y1 = next_idx, next_val
                interpolated = y0 + (y1 - y0) * (i - x0) / (x1 - x0)
                result[i] = interpolated
                imputed_count += 1
            elif prev_idx is not None:
                # Use previous value
                result[i] = prev_val
                imputed_count += 1
            elif next_idx is not None:
                # Use next value
                result[i] = next_val
                imputed_count += 1
    
    return result, imputed_count

def main():
    method, values = read_input()
    
    if method == 'mean':
        imputed_data, imputed_count = impute_mean(values)
    elif method == 'median':
        imputed_data, imputed_count = impute_median(values)
    elif method == 'linear':
        imputed_data, imputed_count = impute_linear(values)
    else:
        imputed_data, imputed_count = values, 0
    
    output = {
        "imputed_data": imputed_data,
        "imputed_count": imputed_count,
        "method_used": method
    }
    
    print(json.dumps(output, separators=(',', ':')))

if __name__ == "__main__":
    main()